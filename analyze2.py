#!/usr/bin/env python3
import re
from pathlib import Path
from collections import defaultdict
import pandas as pd

class AmandroidBatchParser:
    def __init__(self):
        self.source_patterns = {
            'geographic_location': [r'LocationManager', r'getLastKnownLocation',
                                    r'getLatitude', r'getLongitude', 
                                    r'GPS', 
                                    r'FusedLocationProviderClient', 
                                    r'ACCESS_.*_LOCATION'],
            'microphone': [r'MediaRecorder', r'AudioRecord', 
                           r'startRecording', 
                           r'RECORD_AUDIO', r'SpeechRecognizer'],
            'device_identifiers': [r'getDeviceId', r'getSubscriberId', 
                                   r'IMEI', r'IMSI', r'getAndroidId', 
                                   r'TelephonyManager', 
                                   r'getMacAddress', r'getAdvertisingIdInfo', 
                                   r'READ_PHONE_STATE'],
            'icc_sources': [r'Intent;\.get', 
                            r'getExtras', r'get.*Extra'],
            'account_auth': [r'AccountManager', 
                             r'getAuthToken', r'getAccounts']
        }
        
        self.sink_patterns = {
            'file': [r'FileOutputStream', r'FileWriter', 
                     r'SharedPreferences', r'put.*', r'write\(', 
                     r'commit\(\)', r'apply\(\)'],
            'network': [r'HttpURLConnection', r'HttpClient', r'Socket', 
                        r'sendTextMessage', r'http', r'getOutputStream', r'send'],
            'log': [r'Log;\.', r'println'],
            'icc_sinks': [r'startActivity', r'sendBroadcast', 
                          r'startService', r'setResult']
        }
    
    def find_apps(self, outputs_dir):
        apps = []
        for app_dir in Path(outputs_dir).iterdir():
            if app_dir.is_dir():
                appdata = app_dir / 'result' / 'AppData.txt'
                if appdata.exists():
                    apps.append((app_dir.name, str(appdata)))
                    print(f"Found: {app_dir.name}")
        return apps
    
    def parse_file(self, file_path):
        try:
            text = open(file_path, 'r', encoding='utf-8', errors='ignore').read()
        except Exception as e:
            print(f"Error: {e}")
            return None
        
        sources = re.findall(r'<Descriptors:\s*([^>]+)>', 
                            re.search(r'Sources found:(.*?)Sinks found:', text, re.DOTALL).group(1) 
                            if re.search(r'Sources found:(.*?)Sinks found:', text, re.DOTALL) else '')
        
        sinks = re.findall(r'<Descriptors:\s*([^>]+)>', 
                          re.search(r'Sinks found:(.*?)(?:Discovered taint paths|$)', text, re.DOTALL).group(1)
                          if re.search(r'Sinks found:(.*?)(?:Discovered taint paths|$)', text, re.DOTALL) else '')
        
        return {
            'sources': sources,
            'sinks': sinks,
            'taint_paths': len(re.findall(r'TaintPath:', text))
        }
    
    def categorize(self, items, patterns):
        cats = defaultdict(int)
        for item in items:
            matched = False
            for cat, pats in patterns.items():
                if any(re.search(p, item, re.IGNORECASE) for p in pats):
                    cats[cat] += 1
                    matched = True
                    break
            if not matched:
                cats['uncategorized'] += 1
        return dict(cats)
    
    def analyze_app(self, app_name, file_path):
        print(f"Analyzing {app_name}...")
        parsed = self.parse_file(file_path)
        if not parsed:
            return None
        
        src_cats = self.categorize(parsed['sources'], self.source_patterns)
        snk_cats = self.categorize(parsed['sinks'], self.sink_patterns)
        
        return {
            'app_name': app_name,
            'total_sources': len(parsed['sources']),
            'total_sinks': len(parsed['sinks']),
            'taint_paths': parsed['taint_paths'],
            'geo_location': src_cats.get('geographic_location', 0),
            'microphone': src_cats.get('microphone', 0),
            'device_id': src_cats.get('device_identifiers', 0),
            'icc_sources': src_cats.get('icc_sources', 0),
            'account_auth': src_cats.get('account_auth', 0),
            'file_sink': snk_cats.get('file', 0),
            'network_sink': snk_cats.get('network', 0),
            'log_sink': snk_cats.get('log', 0),
            'icc_sinks': snk_cats.get('icc_sinks', 0)
        }
    
    def batch_analyze(self, outputs_dir):
        apps = self.find_apps(outputs_dir)
        print(f"\nFound {len(apps)} apps\n")
        return [r for r in (self.analyze_app(name, path) for name, path in apps) if r]

def main():
    parser = AmandroidBatchParser()
    results = parser.batch_analyze('./outputs7')
    
    if results:
        df = pd.DataFrame(results)
        df.columns = ['App Name', 'Total Sources', 'Total Sinks', 'Taint Paths',
                      'Geo Location', 'Microphone', 'Device ID', 
                      'ICC Sources', 'Account/Auth',
                      'File', 'Network', 'Log', 'ICC Sinks']
        df.to_csv('amandroid_analysis_results.csv', index=False)
        print(f"\nSaved to amandroid_analysis_results.csv")

if __name__ == "__main__":
    main()
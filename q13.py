#!/usr/bin/env python3
import re
from pathlib import Path
from collections import defaultdict
import pandas as pd

class AmandroidPathAnalyzer:
    def __init__(self):
        self.source_patterns = {
            'geographic_location': [r'LocationManager', r'getLastKnownLocation', 
                                    r'getLatitude', r'getLongitude', r'GPS'],
            'microphone': [r'MediaRecorder', r'AudioRecord', 
                           r'startRecording', r'RECORD_AUDIO'],
            'device_identifiers': [r'getDeviceId', r'getSubscriberId',
                                   r'IMEI', r'IMSI', r'getAndroidId', r'getMacAddress'],
            'icc_sources': [r'Intent;\.get', r'getExtras', r'getStringExtra'],
            'account_auth': [r'AccountManager', r'getAuthToken']
        }
        self.sink_patterns = {
            'file': [r'FileOutputStream', r'FileWriter', 
                     r'SharedPreferences', r'putString', r'write\('],
            'network': [r'HttpURLConnection', r'HttpClient', 
                        r'Socket;', r'sendTextMessage', r'sendBroadcast'],
            'log': [r'Log;\.v', r'Log;\.d', 
                    r'Log;\.e', r'println'],
            'icc_sinks': [r'startActivity', r'sendBroadcast', 
                          r'startService', r'setResult']
        }
    
    def categorize(self, descriptor, patterns):
        for category, pattern_list in patterns.items():
            if any(re.search(p, descriptor, re.IGNORECASE) for p in pattern_list):
                return category
        return 'other'
    
    def parse_taint_paths(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []
        
        match = re.search(r'Discovered taint paths are listed below:(.*)', text, re.DOTALL)
        if not match:
            return []
        
        paths = []
        for block in re.split(r'\n\s*TaintPath:', match.group(1)):
            src = re.search(r'Source:\s*<Descriptors:\s*([^:]+):\s*([^>]+)>', block)
            snk = re.search(r'Sink:\s*<Descriptors:\s*([^:]+):\s*([^>]+)>', block)
            
            if src and snk:
                paths.append({
                    'source_sig': src.group(2).strip(),
                    'sink_sig': snk.group(2).strip()
                })
        
        return paths
    
    def build_matrix(self, paths):
        matrix = defaultdict(lambda: defaultdict(int))
        for path in paths:
            src_cat = self.categorize(path['source_sig'], self.source_patterns)
            snk_cat = self.categorize(path['sink_sig'], self.sink_patterns)
            matrix[src_cat][snk_cat] += 1
        return matrix
    
    def create_table(self, matrix):
        sources = ['geographic_location', 'microphone', 
                   'device_identifiers', 'icc_sources', 'account_auth', 'other']
        sinks = ['file', 'network', 'log', 'icc_sinks', 'other']
        
        data = []
        for src in sources:
            row = {'Source': src.replace('_', ' ').title()}
            row.update({s.title(): matrix.get(src, {}).get(s, 0) for s in sinks})
            row['Total'] = sum(row[s.title()] for s in sinks)
            data.append(row)
        
        totals = {'Source': 'TOTAL'}
        totals.update({s.title(): sum(matrix.get(src, {}).get(s, 0) for src in sources) for s in sinks})
        totals['Total'] = sum(totals[s.title()] for s in sinks)
        data.append(totals)
        
        return pd.DataFrame(data)
    
    def find_apps(self, outputs_dir):
        apps = []
        for app_dir in Path(outputs_dir).iterdir():
            if app_dir.is_dir():
                appdata = app_dir / 'result' / 'AppData.txt'
                if appdata.exists():
                    apps.append((app_dir.name, str(appdata)))
        return apps
    
    def batch_analyze(self, outputs_dir):
        apps = self.find_apps(outputs_dir)
        print(f"Found {len(apps)} apps\n")
        
        results = []
        for app_name, file_path in apps:
            paths = self.parse_taint_paths(file_path)
            if paths:
                print(f"{app_name}: {len(paths)} paths")
                results.append({
                    'app_name': app_name,
                    'matrix': self.build_matrix(paths)
                })
        return results

def generate_report(results, output_file='report.txt'):
    analyzer = AmandroidPathAnalyzer()
    with open(output_file, 'w') as f:
        f.write("AMANDROID TAINT PATH ANALYSIS\n" + "="*80 + "\n\n")
        for result in results:
            f.write(f"\nApp: {result['app_name']}\n" + "="*80 + "\n")
            f.write(analyzer.create_table(result['matrix']).to_string(index=False) + "\n\n")
    print(f"Report saved: {output_file}")

def main():
    analyzer = AmandroidPathAnalyzer()
    results = analyzer.batch_analyze('./outputs7')
    if results:
        generate_report(results, 'question_1.3_report.txt')

if __name__ == "__main__":
    main()
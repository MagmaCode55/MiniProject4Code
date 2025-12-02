#!/usr/bin/env python3

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.patches as mpatches

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

data = {
    'App': [
        'robyte-82',
        'safesurfer-44',
        'SpanishTranslate-159',
        'iss_free-54604',
        'castbrowser-79',
        'vvm-91528',
        'newsbreak-314',
        'dating-16'
    ],
    'Total_Paths': [31, 185, 3, 35, 65, 554, 12, 174],
    
    'geo_file': [0, 0, 0, 0, 0, 0, 0, 3],
    'geo_network': [0, 0, 0, 0, 0, 0, 0, 0],
    'geo_log': [0, 0, 0, 0, 0, 0, 0, 2],
    'geo_icc': [0, 0, 0, 0, 0, 0, 0, 2],
    'geo_other': [0, 0, 0, 0, 0, 0, 0, 2],
    
    'device_file': [0, 0, 0, 0, 0, 32, 0, 0],
    'device_network': [0, 0, 0, 0, 0, 2, 0, 0],
    'device_log': [0, 0, 0, 0, 0, 359, 0, 0],
    'device_icc': [0, 0, 0, 0, 0, 2, 0, 0],
    'device_other': [0, 0, 0, 0, 0, 2, 0, 0],
    
    'icc_file': [0, 4, 0, 9, 0, 8, 0, 0],
    'icc_network': [6, 0, 0, 0, 0, 0, 0, 0],
    'icc_log': [15, 170, 0, 24, 0, 119, 0, 0],
    'icc_icc': [0, 0, 0, 0, 0, 0, 0, 0],
    'icc_other': [0, 2, 0, 0, 0, 0, 0, 0],
    
    'other_file': [0, 0, 0, 2, 2, 0, 2, 10],
    'other_network': [0, 1, 1, 0, 0, 0, 0, 0],
    'other_log': [10, 1, 0, 0, 63, 30, 10, 152],
    'other_icc': [0, 8, 0, 0, 0, 2, 0, 5],
    'other_other': [0, 8, 2, 0, 0, 2, 0, 5]
}

df = pd.DataFrame(data)

def source_sink_flow_matrix():
    
    fig, ax = plt.subplots(figsize=(12, 10))
    sources = ['Geographic Location', 'Device Identifiers', 'ICC Sources', 'Other']
    sinks = ['File', 'Network', 'Log', 'ICC Sinks', 'Other']
    
    matrix = np.array([
        
        [df['geo_file'].sum(), df['geo_network'].sum(), df['geo_log'].sum(), 
         df['geo_icc'].sum(), df['geo_other'].sum()],
        
        [df['device_file'].sum(), df['device_network'].sum(), df['device_log'].sum(),
         df['device_icc'].sum(), df['device_other'].sum()],
        
        [df['icc_file'].sum(), df['icc_network'].sum(), df['icc_log'].sum(),
         df['icc_icc'].sum(), df['icc_other'].sum()],
        
        [df['other_file'].sum(), df['other_network'].sum(), df['other_log'].sum(),
         df['other_icc'].sum(), df['other_other'].sum()]
    ])
    
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    
    for i in range(len(sources)):
        for j in range(len(sinks)):
            value = matrix[i, j]
            text_color = 'white' if value > matrix.max() * 0.5 else 'black'
            text = ax.text(j, i, int(value), ha="center", va="center",
                          color=text_color, fontsize=12, fontweight='bold')
    
    # Labels and title
    ax.set_xticks(np.arange(len(sinks)))
    ax.set_yticks(np.arange(len(sources)))
    ax.set_xticklabels(sinks, fontsize=11, fontweight='bold')
    ax.set_yticklabels(sources, fontsize=11, fontweight='bold')
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    ax.set_title('Aggregate Data Flow Matrix\nAll Applications Combined', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Sink Category', fontsize=13, fontweight='bold', labelpad=10)
    ax.set_ylabel('Source Category', fontsize=13, fontweight='bold', labelpad=10)
    
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Number of Paths', rotation=270, labelpad=20, 
                   fontsize=12, fontweight='bold')
    
    ax.set_xticks(np.arange(len(sinks))-.5, minor=True)
    ax.set_yticks(np.arange(len(sources))-.5, minor=True)
    ax.grid(which="minor", color="gray", linestyle='-', linewidth=2)
    
    plt.tight_layout()
    plt.savefig('flow_matrix.png', dpi=300, bbox_inches='tight')
    print("Generated: flow_matrix.png")
    plt.close()
    
if __name__ == "__main__":
    source_sink_flow_matrix()
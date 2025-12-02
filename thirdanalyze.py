#!/usr/bin/env python3

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

sns.set_style("whitegrid")
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 13
plt.rcParams['axes.titlesize'] = 15
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11

apps = [
    'tinybyteapps',
    'SpanishTranslate',
    'nicedayapps',
    'metropcs',
    'particlenews',
    'dating',
]

data = {
    'App': apps,
    'Total Sources': [37, 12, 38, 110, 105, 43],
    'Geographic Location': [0, 0, 0, 0, 2, 2],
    'Microphone': [0, 0, 0, 0, 0, 0],
    'Device ID': [0, 0, 0, 13, 0, 0],
    'ICC Sources': [26, 9, 35, 86, 99, 27],
    'Account/Auth': [0, 0, 0, 0, 0, 0],
    'Total Sinks': [227, 33, 244, 927, 177,423],
    'File': [30, 12, 36, 266, 28, 46],
    'Network': [3, 12, 8, 40, 10, 28],
    'Log': [191, 0, 182, 612, 134, 347],
    'ICC Sinks': [2, 7, 17, 9, 4, 0]
}

df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(14, 7))
source_categories = ['Geographic Location', 'Microphone', 'Device ID', 'ICC Sources', 'Account/Auth']
x = np.arange(len(apps))
width = 0.15
colors_multi = ['#3498db', '#9b59b6', '#e91e63', '#f39c12', '#16a085']

for i, (category, color) in enumerate(zip(source_categories, colors_multi)):
    offset = width * (i - 2)
    bars = ax.bar(x + offset, df[category], width, label=category, 
                   color=color, edgecolor='black', linewidth=1, alpha=0.85)
    ax.bar_label(bars)

ax.set_title('Source Categories Distribution by Application', fontweight='bold', fontsize=16)
ax.set_ylabel('Count', fontweight='bold')
ax.set_xlabel('Application', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(apps, rotation=45, ha='right')
ax.legend(fontsize=10, ncol=2)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('fig3_source_categories_grouped.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('fig3_source_categories_grouped.pdf', bbox_inches='tight', facecolor='white')
plt.close()
print("Saved: fig3_source_categories_grouped.png / .pdf")

fig, ax = plt.subplots(figsize=(14, 7))
sink_categories = ['File', 'Network', 'Log', 'ICC Sinks']
colors_sinks_multi = ['#e67e22', '#27ae60', '#c0392b', '#8e44ad']

for i, (category, color) in enumerate(zip(sink_categories, colors_sinks_multi)):
    offset = width * (i - 1.5)
    bars = ax.bar(x + offset, df[category], width, label=category, 
                   color=color, edgecolor='black', linewidth=1, alpha=0.85)
    ax.bar_label(bars)

ax.set_title('Sink Categories Distribution by Application', fontweight='bold', fontsize=16)
ax.set_ylabel('Count', fontweight='bold')
ax.set_xlabel('Application', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(apps, rotation=45, ha='right')
ax.legend(fontsize=11, ncol=2)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('fig4_sink_categories_grouped.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('fig4_sink_categories_grouped.pdf', bbox_inches='tight', facecolor='white')
plt.close()
print("Saved: fig4_sink_categories_grouped.png / .pdf")

#!/usr/bin/env python3
"""
Figuras 12, 13, 14 - V3 Color + B/W
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, confusion_matrix
from scipy.stats import mannwhitneyu
import warnings
warnings.filterwarnings('ignore')

# Paletas
COLOR_MODERN = {
    'primary': '#2E5C8A', 'secondary': '#7B8FA1', 'accent': '#D4A373',
    'success': '#5E8B7E', 'warning': '#C9A227', 'alert': '#A44A3F',
    'neutral': '#8B8178', 'dark': '#2C3539', 'light': '#F5F5F0',
    'or_main': '#1B4965', 'or_light': '#5FA8D3', 'or_accent': '#BEE9E8',
    'clinical': '#C9A227', 'and_rule': '#A44A3F',
}

plt.rcParams.update({
    'font.size': 11, 'axes.titlesize': 13, 'axes.labelsize': 11,
    'figure.facecolor': 'white', 'axes.facecolor': 'white',
    'axes.edgecolor': '#2C3539', 'text.color': '#2C3539',
    'grid.color': '#E0E0E0', 'grid.linestyle': '-', 'grid.linewidth': 0.5,
})

# Cargar datos
df = pd.read_csv('/home/xiu/Desktop/cinder-main/cinder-main/db/db-cinder-tox-mod.csv')
df.columns = [c.strip().lower() for c in df.columns]
df = df.dropna(subset=['news2_score']).copy()
y_true = (df['news2_score'] >= 5).astype(int)

import os
os.makedirs('figuras_v3_color', exist_ok=True)
os.makedirs('figuras_v3_bw', exist_ok=True)

# ============================================================
# FIGURA 12: CONFUSION MATRICES (3 paneles)
# ============================================================
print("Figura 12: Confusion Matrices...")

regla_or = ((df['fr'] > 22.5) | (df['tas'] <= 91.5)).astype(int)
regla_and = ((df['fr'] > 22.5) & (df['tas'] <= 91.5)).astype(int)
pred_clinico = df['nivel_atencion'].isin(['I', 'II']).astype(int)

# COLOR
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

predictores = [
    (regla_or, 'CINDER OR\n(Screening)', COLOR_MODERN['or_main']),
    (pred_clinico, 'Clinical\nPriority', COLOR_MODERN['clinical']),
    (regla_and, 'CINDER AND\n(Alert)', COLOR_MODERN['and_rule']),
]

for ax, (pred, title, color) in zip(axes, predictores):
    cm = confusion_matrix(y_true, pred)
    tn, fp, fn, tp = cm.ravel()
    
    # Normalizar para visualización
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    im = ax.imshow(cm_norm, cmap='Blues', vmin=0, vmax=1)
    
    # Texto
    labels = [['TN\n{}'.format(tn), 'FP\n{}'.format(fp)],
              ['FN\n{}'.format(fn), 'TP\n{}'.format(tp)]]
    
    for i in range(2):
        for j in range(2):
            ax.text(j, i, labels[i][j], ha='center', va='center',
                   fontsize=14, fontweight='bold', color='white' if cm_norm[i,j] > 0.5 else 'black')
    
    ax.set_title(title, fontsize=12, fontweight='bold', color=color)
    ax.set_xlabel('Predicted', fontsize=10)
    ax.set_ylabel('Gold Standard', fontsize=10)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['No Severe', 'Severe'])
    ax.set_yticklabels(['No Severe', 'Severe'])

fig.suptitle('Confusion Matrices (n=188, NEWS-2≥5)', fontsize=14, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig('figuras_v3_color/Fig12_ConfusionMatrices_Color.png', dpi=300, bbox_inches='tight')
fig.savefig('figuras_v3_color/Fig12_ConfusionMatrices_Color.svg', bbox_inches='tight')

# B/W
fig_bw, axes_bw = plt.subplots(1, 3, figsize=(15, 5))
for ax, (pred, title, _) in zip(axes_bw, predictores):
    cm = confusion_matrix(y_true, pred)
    tn, fp, fn, tp = cm.ravel()
    
    # B/W con patrones
    from matplotlib.patches import Rectangle
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    
    valores = [[tn, fp], [fn, tp]]
    tipos = [['TN', 'FP'], ['FN', 'TP']]
    
    for i in range(2):
        for j in range(2):
            rect = Rectangle((j-0.5, i-0.5), 1, 1, linewidth=2, 
                           edgecolor='black', facecolor='white')
            ax.add_patch(rect)
            ax.text(j, i, f'{tipos[i][j]}\n{valores[i][j]}', ha='center', va='center',
                   fontsize=14, fontweight='bold', color='black')
    
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel('Predicted', fontsize=10)
    ax.set_ylabel('Gold Standard', fontsize=10)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['No Severe', 'Severe'])
    ax.set_yticklabels(['No Severe', 'Severe'])
    ax.set_aspect('equal')

fig_bw.suptitle('Confusion Matrices (n=188, NEWS-2≥5)', fontsize=14, fontweight='bold', y=1.02)
fig_bw.tight_layout()
fig_bw.savefig('figuras_v3_bw/Fig12_ConfusionMatrices_BW.png', dpi=300, bbox_inches='tight')
fig_bw.savefig('figuras_v3_bw/Fig12_ConfusionMatrices_BW.svg', bbox_inches='tight')

plt.close('all')
print("  ✅ Fig12")

# ============================================================
# FIGURA 13: SENSITIVITY BY TOXIC AGENT
# ============================================================
print("Figura 13: Sensitivity by Toxic Agent...")

grupos = ['benzodiacepina', 'alcohol', 'antidepresivo', 'antipsicotico']
labels_grupos = ['Benzodiazepines', 'Alcohol', 'Antidepressants', 'Antipsychotics']

# Calcular sensibilidades
sens_or, sens_cl, sens_and = [], [], []

for grupo in grupos:
    subset = df[df['tipo_toxico_principal'] == grupo]
    if len(subset) == 0:
        sens_or.append(0); sens_cl.append(0); sens_and.append(0)
        continue
    
    y_sub = (subset['news2_score'] >= 5).astype(int)
    regla_or_sub = ((subset['fr'] > 22.5) | (subset['tas'] <= 91.5)).astype(int)
    regla_and_sub = ((subset['fr'] > 22.5) & (subset['tas'] <= 91.5)).astype(int)
    pred_clinico_sub = subset['nivel_atencion'].isin(['I', 'II']).astype(int)
    
    def calc_sens(y, pred):
        cm = confusion_matrix(y, pred)
        if cm.shape != (2, 2):
            return 0
        tn, fp, fn, tp = cm.ravel()
        return tp / (tp + fn) * 100 if (tp + fn) > 0 else 0
    
    sens_or.append(calc_sens(y_sub, regla_or_sub))
    sens_cl.append(calc_sens(y_sub, pred_clinico_sub))
    sens_and.append(calc_sens(y_sub, regla_and_sub))

# COLOR
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(labels_grupos))
width = 0.25

bars1 = ax.bar(x - width, sens_or, width, label='CINDER OR', color=COLOR_MODERN['or_main'], 
               edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x, sens_cl, width, label='Clinical', color=COLOR_MODERN['clinical'],
               edgecolor='black', linewidth=1.5)
bars3 = ax.bar(x + width, sens_and, width, label='CINDER AND', color=COLOR_MODERN['and_rule'],
               edgecolor='black', linewidth=1.5)

ax.set_ylabel('Sensitivity (%)', fontsize=12, fontweight='bold')
ax.set_title('Sensitivity by Toxic Agent\n(n=188, NEWS-2≥5 as Gold Standard)', 
             fontsize=13, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels_grupos, fontsize=10)
ax.legend(fontsize=10, framealpha=0.95)
ax.set_ylim(0, 100)
ax.yaxis.grid(True, alpha=0.3)

# Labels
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=8)

fig.tight_layout()
fig.savefig('figuras_v3_color/Fig13_SensitivityByToxic_Color.png', dpi=300, bbox_inches='tight')
fig.savefig('figuras_v3_color/Fig13_SensitivityByToxic_Color.svg', bbox_inches='tight')

# B/W
fig_bw, ax_bw = plt.subplots(figsize=(12, 6))

bars1_bw = ax_bw.bar(x - width, sens_or, width, label='CINDER OR', color='#333333',
                    edgecolor='black', linewidth=1.5, hatch='///')
bars2_bw = ax_bw.bar(x, sens_cl, width, label='Clinical', color='#666666',
                    edgecolor='black', linewidth=1.5, hatch='...')
bars3_bw = ax_bw.bar(x + width, sens_and, width, label='CINDER AND', color='#999999',
                    edgecolor='black', linewidth=1.5, hatch='xxx')

ax_bw.set_ylabel('Sensitivity (%)', fontsize=12, fontweight='bold')
ax_bw.set_title('Sensitivity by Toxic Agent\n(n=188, NEWS-2≥5 as Gold Standard)', 
                fontsize=13, fontweight='bold')
ax_bw.set_xticks(x)
ax_bw.set_xticklabels(labels_grupos, fontsize=10)
ax_bw.legend(fontsize=10, framealpha=0.95)
ax_bw.set_ylim(0, 100)
ax_bw.yaxis.grid(True, alpha=0.3)

for bars in [bars1_bw, bars2_bw, bars3_bw]:
    for bar in bars:
        height = bar.get_height()
        ax_bw.text(bar.get_x() + bar.get_width()/2., height + 2,
                   f'{height:.1f}%', ha='center', va='bottom', fontsize=8, color='black')

fig_bw.tight_layout()
fig_bw.savefig('figuras_v3_bw/Fig13_SensitivityByToxic_BW.png', dpi=300, bbox_inches='tight')
fig_bw.savefig('figuras_v3_bw/Fig13_SensitivityByToxic_BW.svg', bbox_inches='tight')

plt.close('all')
print("  ✅ Fig13")

# ============================================================
# FIGURA 14: NEWS-2 BY TOXIC AGENT
# ============================================================
print("Figura 14: NEWS-2 by Toxic Agent...")

means, stds, n_graves, prevalencias = [], [], [], []

for grupo in grupos:
    subset = df[df['tipo_toxico_principal'] == grupo]
    if len(subset) > 0:
        means.append(subset['news2_score'].mean())
        stds.append(subset['news2_score'].std())
        n_g = (subset['news2_score'] >= 5).sum()
        n_graves.append(n_g)
        prevalencias.append(n_g / len(subset) * 100)
    else:
        means.append(0); stds.append(0); n_graves.append(0); prevalencias.append(0)

# COLOR
fig, ax1 = plt.subplots(figsize=(12, 6))

x = np.arange(len(labels_grupos))
width = 0.35

# Barras de NEWS-2 mean
bars = ax1.bar(x, means, width, yerr=stds, color=COLOR_MODERN['primary'],
               edgecolor='black', linewidth=1.5, capsize=5, alpha=0.8,
               label='Mean NEWS-2')

ax1.set_ylabel('NEWS-2 Score (mean ± SD)', fontsize=12, fontweight='bold', color=COLOR_MODERN['primary'])
ax1.set_title('NEWS-2 Distribution and Severity Rate by Toxic Agent\n(n=188)', 
              fontsize=13, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(labels_grupos, fontsize=10)
ax1.tick_params(axis='y', labelcolor=COLOR_MODERN['primary'])
ax1.yaxis.grid(True, alpha=0.3)

# Labels en barras
for bar, mean, std in zip(bars, means, stds):
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + std + 0.3,
             f'{mean:.1f}±{std:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Eje secundario: prevalencia
ax2 = ax1.twinx()
line = ax2.plot(x, prevalencias, 'o-', color=COLOR_MODERN['alert'], 
                linewidth=3, markersize=10, label='% Severe (NEWS-2≥5)')
ax2.set_ylabel('Severe Cases (%)', fontsize=12, fontweight='bold', color=COLOR_MODERN['alert'])
ax2.tick_params(axis='y', labelcolor=COLOR_MODERN['alert'])
ax2.set_ylim(0, max(prevalencias) * 1.2)

# Labels en puntos
for i, (xi, prev) in enumerate(zip(x, prevalencias)):
    ax2.text(xi, prev + 2, f'{prev:.1f}%\n(n={n_graves[i]})', 
             ha='center', va='bottom', fontsize=9, color=COLOR_MODERN['alert'], fontweight='bold')

# Leyendas combinadas
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10, framealpha=0.95)

fig.tight_layout()
fig.savefig('figuras_v3_color/Fig14_NEWS2ByToxic_Color.png', dpi=300, bbox_inches='tight')
fig.savefig('figuras_v3_color/Fig14_NEWS2ByToxic_Color.svg', bbox_inches='tight')

# B/W
fig_bw, ax1_bw = plt.subplots(figsize=(12, 6))

bars_bw = ax1_bw.bar(x, means, width, yerr=stds, color='#CCCCCC',
                    edgecolor='black', linewidth=1.5, capsize=5, hatch='///')

ax1_bw.set_ylabel('NEWS-2 Score (mean ± SD)', fontsize=12, fontweight='bold')
ax1_bw.set_title('NEWS-2 Distribution and Severity Rate by Toxic Agent\n(n=188)', 
                 fontsize=13, fontweight='bold')
ax1_bw.set_xticks(x)
ax1_bw.set_xticklabels(labels_grupos, fontsize=10)
ax1_bw.yaxis.grid(True, alpha=0.3)

for bar, mean, std in zip(bars_bw, means, stds):
    ax1_bw.text(bar.get_x() + bar.get_width()/2., bar.get_height() + std + 0.3,
                f'{mean:.1f}±{std:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

ax2_bw = ax1_bw.twinx()
line_bw = ax2_bw.plot(x, prevalencias, 's--', color='black', 
                      linewidth=2.5, markersize=8, markerfacecolor='white',
                      label='% Severe (NEWS-2≥5)')
ax2_bw.set_ylabel('Severe Cases (%)', fontsize=12, fontweight='bold')
ax2_bw.set_ylim(0, max(prevalencias) * 1.2)

for i, (xi, prev) in enumerate(zip(x, prevalencias)):
    ax2_bw.text(xi, prev + 2, f'{prev:.1f}%\n(n={n_graves[i]})', 
                ha='center', va='bottom', fontsize=9, color='black', fontweight='bold')

lines1_bw, labels1_bw = ax1_bw.get_legend_handles_labels()
lines2_bw, labels2_bw = ax2_bw.get_legend_handles_labels()
ax1_bw.legend(lines1_bw + lines2_bw, labels1_bw + labels2_bw, loc='upper left', fontsize=10)

fig_bw.tight_layout()
fig_bw.savefig('figuras_v3_bw/Fig14_NEWS2ByToxic_BW.png', dpi=300, bbox_inches='tight')
fig_bw.savefig('figuras_v3_bw/Fig14_NEWS2ByToxic_BW.svg', bbox_inches='tight')

plt.close('all')
print("  ✅ Fig14")

print("\n🎉 TODAS las figuras v3 generadas!")
color_files = os.listdir('figuras_v3_color')
bw_files = os.listdir('figuras_v3_bw')
print(f"Color: {len(color_files)} archivos")
print(f"B/W: {len(bw_files)} archivos")


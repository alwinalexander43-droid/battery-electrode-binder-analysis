"""
Battery Electrode & Binder Material Analysis
Script 03: Coulombic Efficiency & Internal Resistance (DCIR) Analysis
Author: Alwin Alexander Rajan
MSc Materials Engineering, Chalmers University of Technology

Coulombic Efficiency (CE) is a critical indicator of side reactions
and SEI stability. DCIR (DC Internal Resistance) growth indicates
degradation of electrode-electrolyte interfaces and binder integrity.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'grid.alpha': 0.3,
    'figure.dpi': 150, 'savefig.dpi': 200, 'savefig.bbox': 'tight'
})

COLORS = {'PVDF': '#1F4E79', 'UV-Binder': '#C0392B', 'SBR': '#27AE60'}
CHEM_MARKER = {'LFP': 'o', 'NMC': 's', 'LFMP': '^'}

df = pd.read_csv('data/cycling_data.csv')

# ── Fig 1: Coulombic Efficiency ────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)
fig.suptitle('Coulombic Efficiency vs Cycle Number\n(Indicator of SEI Stability & Side Reactions)',
             fontsize=13, fontweight='bold')

for ax, chem in zip(axes, ['LFP', 'NMC', 'LFMP']):
    subset = df[df['Chemistry'] == chem]
    for binder in subset['Binder'].unique():
        b = subset[subset['Binder'] == binder]
        smooth = b['Coulombic_Efficiency_%'].rolling(7, center=True).mean()
        ax.plot(b['Cycle'], smooth, color=COLORS[binder],
                linewidth=1.8, label=binder, alpha=0.9)
        ax.fill_between(b['Cycle'],
                        smooth - 0.1, smooth + 0.1,
                        color=COLORS[binder], alpha=0.08)

    ax.axhline(99.9, color='gray', linestyle='--', linewidth=1, alpha=0.6)
    ax.text(5, 99.91, '99.9% CE', color='gray', fontsize=8)
    ax.set_title(f'{chem}', fontweight='bold', fontsize=12)
    ax.set_xlabel('Cycle Number', fontsize=10)
    ax.set_ylabel('Coulombic Efficiency (%)', fontsize=10)
    ax.set_ylim(99.0, 100.1)
    ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig('plots/07_coulombic_efficiency.png')
plt.close()
print("✓ Plot 7: Coulombic Efficiency saved")

# ── Fig 2: DCIR Growth ────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('DC Internal Resistance (DCIR) Growth During Cycling\n(Binder Integrity & Electrode-Electrolyte Interface)',
             fontsize=13, fontweight='bold')

# Left: LFP all binders
ax = axes[0]
subset = df[df['Chemistry'] == 'LFP']
for binder in subset['Binder'].unique():
    b = subset[subset['Binder'] == binder]
    smooth = b['DCIR_mOhm'].rolling(7, center=True).mean()
    ax.plot(b['Cycle'], smooth, color=COLORS[binder],
            linewidth=2, label=binder)
    ax.fill_between(b['Cycle'], smooth*0.98, smooth*1.02,
                    color=COLORS[binder], alpha=0.1)
ax.set_title('LFP — All Binders', fontweight='bold')
ax.set_xlabel('Cycle Number')
ax.set_ylabel('DCIR (mΩ)')
ax.legend()

# Right: UV-Binder across chemistries
ax = axes[1]
CHEM_COLORS = {'LFP': '#1F4E79', 'NMC': '#C0392B', 'LFMP': '#27AE60'}
for chem in ['LFP', 'NMC', 'LFMP']:
    subset = df[(df['Chemistry'] == chem) & (df['Binder'] == 'UV-Binder')]
    smooth = subset['DCIR_mOhm'].rolling(7, center=True).mean()
    ax.plot(subset['Cycle'], smooth, color=CHEM_COLORS[chem],
            linewidth=2, label=f'{chem} / UV-Binder',
            marker=CHEM_MARKER[chem], markevery=30, markersize=5)
ax.set_title('UV-Binder — All Chemistries', fontweight='bold')
ax.set_xlabel('Cycle Number')
ax.set_ylabel('DCIR (mΩ)')
ax.legend()

plt.tight_layout()
plt.savefig('plots/08_dcir_growth.png')
plt.close()
print("✓ Plot 8: DCIR Growth saved")

# ── Fig 3: Summary Dashboard ──────────────────────────────────────────
fig = plt.figure(figsize=(16, 10))
fig.suptitle('Battery Performance Dashboard — LFP Electrode Systems\nBinder Comparison: PVDF vs UV-Binder vs SBR',
             fontsize=14, fontweight='bold', y=1.01)

gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

lfp = df[df['Chemistry'] == 'LFP']

# 1. Capacity fade
ax1 = fig.add_subplot(gs[0, :2])
for binder in ['PVDF', 'UV-Binder', 'SBR']:
    b = lfp[lfp['Binder'] == binder]
    smooth = b['Discharge_Capacity_mAh_g'].rolling(5, center=True).mean()
    ax1.plot(b['Cycle'], smooth, color=COLORS[binder], linewidth=2.2, label=binder)
ax1.axhline(lfp[lfp['Binder']=='PVDF']['Discharge_Capacity_mAh_g'].iloc[0]*0.8,
            color='gray', linestyle=':', alpha=0.7)
ax1.set_title('Discharge Capacity Fade', fontweight='bold')
ax1.set_xlabel('Cycle')
ax1.set_ylabel('Capacity (mAh/g)')
ax1.legend()

# 2. Coulombic efficiency
ax2 = fig.add_subplot(gs[0, 2])
for binder in ['PVDF', 'UV-Binder', 'SBR']:
    b = lfp[lfp['Binder'] == binder]
    smooth = b['Coulombic_Efficiency_%'].rolling(7, center=True).mean()
    ax2.plot(b['Cycle'], smooth, color=COLORS[binder], linewidth=1.8, label=binder)
ax2.set_title('Coulombic Efficiency', fontweight='bold')
ax2.set_xlabel('Cycle')
ax2.set_ylabel('CE (%)')
ax2.set_ylim(99.0, 100.1)
ax2.legend(fontsize=8)

# 3. DCIR
ax3 = fig.add_subplot(gs[1, 0])
for binder in ['PVDF', 'UV-Binder', 'SBR']:
    b = lfp[lfp['Binder'] == binder]
    smooth = b['DCIR_mOhm'].rolling(7, center=True).mean()
    ax3.plot(b['Cycle'], smooth, color=COLORS[binder], linewidth=1.8, label=binder)
ax3.set_title('DCIR Growth', fontweight='bold')
ax3.set_xlabel('Cycle')
ax3.set_ylabel('DCIR (mΩ)')
ax3.legend(fontsize=8)

# 4. Capacity retention bar at 200
ax4 = fig.add_subplot(gs[1, 1])
binders_list = ['PVDF', 'UV-Binder', 'SBR']
ret_vals = []
for binder in binders_list:
    b = lfp[lfp['Binder'] == binder]
    init = b['Discharge_Capacity_mAh_g'].iloc[0]
    final = b['Discharge_Capacity_mAh_g'].iloc[-1]
    ret_vals.append((final / init) * 100)

bars = ax4.bar(binders_list, ret_vals,
               color=[COLORS[b] for b in binders_list],
               edgecolor='white', alpha=0.85)
for bar, val in zip(bars, ret_vals):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'{val:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
ax4.axhline(80, color='red', linestyle='--', alpha=0.5)
ax4.set_title('Capacity Retention @ Cycle 200', fontweight='bold')
ax4.set_ylabel('Retention (%)')
ax4.set_ylim(70, 100)

# 5. Binder key metrics table
ax5 = fig.add_subplot(gs[1, 2])
ax5.axis('off')
metrics = []
for binder in binders_list:
    b = lfp[lfp['Binder'] == binder]
    init_cap = b['Discharge_Capacity_mAh_g'].iloc[0]
    final_cap = b['Discharge_Capacity_mAh_g'].iloc[-1]
    avg_ce = b['Coulombic_Efficiency_%'].mean()
    final_dcir = b['DCIR_mOhm'].iloc[-1]
    metrics.append([binder, f'{init_cap:.1f}', f'{final_cap:.1f}',
                    f'{avg_ce:.2f}', f'{final_dcir:.1f}'])

table = ax5.table(
    cellText=metrics,
    colLabels=['Binder', 'Initial\n(mAh/g)', 'Final\n(mAh/g)', 'Avg CE\n(%)', 'DCIR\n(mΩ)'],
    cellLoc='center', loc='center',
    bbox=[0, 0.1, 1, 0.85]
)
table.auto_set_font_size(False)
table.set_fontsize(9)
for (r, c), cell in table.get_celld().items():
    if r == 0:
        cell.set_facecolor('#1F4E79')
        cell.set_text_props(color='white', fontweight='bold')
    elif r % 2 == 0:
        cell.set_facecolor('#EBF3FB')
    cell.set_edgecolor('white')
ax5.set_title('Summary Table', fontweight='bold', pad=10)

plt.savefig('plots/09_dashboard.png', bbox_inches='tight')
plt.close()
print("✓ Plot 9: Dashboard saved")
print("\n✓ Coulombic Efficiency & DCIR Analysis complete")

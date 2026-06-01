"""
Battery Electrode & Binder Material Analysis
Script 01: Capacity Fade & State of Health (SOH) Analysis
Author: Alwin Alexander Rajan
MSc Materials Engineering, Chalmers University of Technology

This script analyses capacity fade and SOH across LFP, NMC, and LFMP
electrode chemistries with three binder systems: PVDF, SBR, and UV-Binder.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

# ── Style ─────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'grid.alpha': 0.3, 'grid.linestyle': '--',
    'figure.dpi': 150, 'savefig.dpi': 200, 'savefig.bbox': 'tight'
})

COLORS = {
    'PVDF':      '#1F4E79',
    'UV-Binder': '#C0392B',
    'SBR':       '#27AE60',
}
MARKERS = {'PVDF': 'o', 'UV-Binder': 's', 'SBR': '^'}
CHEM_COLORS = {'LFP': '#1F4E79', 'NMC': '#C0392B', 'LFMP': '#27AE60'}

df = pd.read_csv('data/cycling_data.csv')

# ── Fig 1: Capacity Fade per Chemistry ────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=False)
fig.suptitle('Discharge Capacity Fade — LFP, NMC & LFMP Electrode Systems\n(UV-Binder vs PVDF vs SBR)',
             fontsize=13, fontweight='bold', y=1.02)

for ax, chem in zip(axes, ['LFP', 'NMC', 'LFMP']):
    subset = df[df['Chemistry'] == chem]
    for binder in subset['Binder'].unique():
        b_data = subset[subset['Binder'] == binder]
        # Rolling average for smooth line
        smooth = b_data['Discharge_Capacity_mAh_g'].rolling(5, center=True).mean()
        ax.plot(b_data['Cycle'], smooth,
                color=COLORS[binder], label=binder,
                linewidth=2.0, marker=MARKERS[binder],
                markevery=25, markersize=5, alpha=0.9)
        # Scatter (raw, faint)
        ax.scatter(b_data['Cycle'], b_data['Discharge_Capacity_mAh_g'],
                   color=COLORS[binder], alpha=0.08, s=4)

    initial_cap = subset.groupby('Binder')['Discharge_Capacity_mAh_g'].first().mean()
    fade_line = initial_cap * 0.80
    ax.axhline(fade_line, color='gray', linestyle=':', linewidth=1.2, alpha=0.7)
    ax.text(205, fade_line + 0.5, '80% SOH', color='gray', fontsize=8, va='bottom')

    ax.set_title(f'{chem} Cathode', fontweight='bold', fontsize=12)
    ax.set_xlabel('Cycle Number', fontsize=10)
    ax.set_ylabel('Discharge Capacity (mAh/g)', fontsize=10)
    ax.legend(fontsize=9, loc='upper right')
    ax.set_xlim(0, 210)

plt.tight_layout()
plt.savefig('plots/01_capacity_fade.png')
plt.close()
print("✓ Plot 1: Capacity Fade saved")

# ── Fig 2: SOH Comparison Bar Chart at cycle 50, 100, 150, 200 ────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('State of Health (SOH) at Key Cycle Milestones', fontsize=13, fontweight='bold')

checkpoints = [50, 100, 150, 200]
for ax, cycle in zip(axes.flatten(), checkpoints):
    cyc_data = df[df['Cycle'] == cycle]
    groups = cyc_data.groupby(['Chemistry', 'Binder'])['SOH_%'].mean().reset_index()
    
    chemistries = ['LFP', 'NMC', 'LFMP']
    binders = ['PVDF', 'UV-Binder', 'SBR']
    x = np.arange(len(chemistries))
    width = 0.25

    for i, binder in enumerate(binders):
        vals = []
        for chem in chemistries:
            row = groups[(groups['Chemistry'] == chem) & (groups['Binder'] == binder)]
            vals.append(float(row['SOH_%'].values[0]) if len(row) > 0 else np.nan)
        bars = ax.bar(x + i * width, vals, width, label=binder,
                      color=COLORS[binder], alpha=0.85, edgecolor='white', linewidth=0.5)
        for bar, val in zip(bars, vals):
            if not np.isnan(val):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                        f'{val:.1f}%', ha='center', va='bottom', fontsize=7.5)

    ax.axhline(80, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax.text(2.9, 80.3, 'EOL (80%)', color='red', fontsize=8)
    ax.set_title(f'Cycle {cycle}', fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(chemistries)
    ax.set_ylabel('SOH (%)')
    ax.set_ylim(70, 102)
    ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig('plots/02_soh_milestones.png')
plt.close()
print("✓ Plot 2: SOH Milestones saved")

# ── Fig 3: Capacity Retention % (normalised) ──────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_title('Normalised Capacity Retention — All Binder Systems\n(All Chemistries Combined)',
             fontsize=13, fontweight='bold')

for chem in ['LFP', 'NMC', 'LFMP']:
    for binder in df['Binder'].unique():
        subset = df[(df['Chemistry'] == chem) & (df['Binder'] == binder)]
        if subset.empty:
            continue
        initial = subset['Discharge_Capacity_mAh_g'].iloc[0]
        retention = (subset['Discharge_Capacity_mAh_g'] / initial) * 100
        smooth = retention.rolling(5, center=True).mean()
        label = f'{chem} / {binder}'
        ls = '--' if binder == 'UV-Binder' else '-'
        ax.plot(subset['Cycle'], smooth, linewidth=1.8, linestyle=ls,
                color=COLORS[binder], alpha=0.8,
                label=label if chem == 'LFP' else '_nolegend_')

ax.axhline(80, color='gray', linestyle=':', linewidth=1.5)
ax.text(205, 80.3, 'EOL', color='gray', fontsize=9)
ax.set_xlabel('Cycle Number', fontsize=11)
ax.set_ylabel('Capacity Retention (%)', fontsize=11)
ax.set_xlim(0, 210)
ax.set_ylim(70, 102)
ax.legend(title='Chemistry / Binder', fontsize=9, loc='lower left')
plt.tight_layout()
plt.savefig('plots/03_capacity_retention.png')
plt.close()
print("✓ Plot 3: Capacity Retention saved")

# ── Degradation Model Fitting ──────────────────────────────────────────
def degradation_model(x, a, b, c):
    return a * np.exp(-b * x) + c

print("\n── Degradation Model Parameters (LFP cells) ──")
print(f"{'Binder':<15} {'a':>8} {'b (rate)':>10} {'c (floor)':>10} {'Cycles to 80%':>15}")
print("-" * 60)

for binder in ['PVDF', 'UV-Binder', 'SBR']:
    subset = df[(df['Chemistry'] == 'LFP') & (df['Binder'] == binder)]
    x = subset['Cycle'].values
    y = subset['SOH_%'].values
    try:
        popt, _ = curve_fit(degradation_model, x, y, p0=[15, 0.005, 82], maxfev=5000)
        a, b, c = popt
        # Estimate cycles to 80% SOH
        cycles_80 = -np.log((80 - c) / a) / b if (80 - c) / a > 0 else '>200'
        print(f"{binder:<15} {a:>8.3f} {b:>10.5f} {c:>10.3f} {str(int(cycles_80)) if isinstance(cycles_80, float) else cycles_80:>15}")
    except Exception:
        print(f"{binder:<15} {'fit failed':>40}")

print("\n✓ Analysis complete — all plots saved to /plots/")

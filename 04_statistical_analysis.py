"""
Battery Electrode & Binder Material Analysis
Script 04: Statistical Binder Comparison & Rate Capability Simulation
Author: Alwin Alexander Rajan
MSc Materials Engineering, Chalmers University of Technology

Statistical analysis comparing binder performance and simulated
rate capability tests (C/5 to 2C) for UV-binder vs PVDF systems.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'grid.alpha': 0.3,
    'figure.dpi': 150, 'savefig.dpi': 200, 'savefig.bbox': 'tight'
})

COLORS = {'PVDF': '#1F4E79', 'UV-Binder': '#C0392B', 'SBR': '#27AE60'}

df = pd.read_csv('data/cycling_data.csv')
np.random.seed(42)

# ── Rate Capability Data ───────────────────────────────────────────────
def rate_capability(initial_cap, binder, c_rates):
    """Simulate capacity at different C-rates"""
    # UV-binder has slightly better rate performance due to thinner coating
    rate_factors = {
        'PVDF':      [1.00, 0.97, 0.93, 0.87, 0.78, 0.65],
        'UV-Binder': [1.00, 0.98, 0.95, 0.90, 0.82, 0.70],
        'SBR':       [1.00, 0.97, 0.92, 0.86, 0.76, 0.62],
    }
    caps = [initial_cap * f + np.random.normal(0, 0.5) for f in rate_factors[binder]]
    return caps

c_rates = [0.1, 0.2, 0.5, 1.0, 1.5, 2.0]
c_labels = ['C/10', 'C/5', '0.5C', '1C', '1.5C', '2C']

# ── Fig 1: Rate Capability ─────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Rate Capability Test — LFP & NMC Electrode Systems\n(UV-Binder vs PVDF)',
             fontsize=13, fontweight='bold')

for ax, chem in zip(axes, ['LFP', 'NMC']):
    init_caps = {'PVDF': 155.0, 'UV-Binder': 158.0, 'SBR': 153.0} if chem == 'LFP' \
        else {'PVDF': 175.0, 'UV-Binder': 178.0}

    for binder, init_cap in init_caps.items():
        caps = rate_capability(init_cap, binder, c_rates)
        # Normalise
        norm_caps = [c / caps[0] * 100 for c in caps]
        ax.plot(range(len(c_rates)), norm_caps, color=COLORS[binder],
                marker='o', linewidth=2.2, markersize=7, label=binder)
        for i, (nc, cap) in enumerate(zip(norm_caps, caps)):
            ax.annotate(f'{cap:.0f}', (i, nc), textcoords='offset points',
                        xytext=(0, 6), fontsize=7.5, color=COLORS[binder],
                        ha='center')

    ax.set_xticks(range(len(c_rates)))
    ax.set_xticklabels(c_labels)
    ax.set_xlabel('C-Rate', fontsize=11)
    ax.set_ylabel('Normalised Capacity (%)', fontsize=11)
    ax.set_title(f'{chem} Rate Capability', fontweight='bold')
    ax.legend(fontsize=10)
    ax.set_ylim(55, 108)

plt.tight_layout()
plt.savefig('plots/10_rate_capability.png')
plt.close()
print("✓ Plot 10: Rate Capability saved")

# ── Fig 2: Statistical Comparison ─────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.suptitle('Statistical Analysis — Capacity Distribution Across Binders\n(LFP, Cycles 100–200)',
             fontsize=13, fontweight='bold')

lfp = df[df['Chemistry'] == 'LFP']
late_cycles = lfp[lfp['Cycle'] >= 100]

for ax, binder in zip(axes, ['PVDF', 'UV-Binder', 'SBR']):
    data = late_cycles[late_cycles['Binder'] == binder]['Discharge_Capacity_mAh_g']
    mean, std = data.mean(), data.std()
    
    ax.hist(data, bins=20, color=COLORS[binder], alpha=0.7,
            edgecolor='white', linewidth=0.5)
    ax.axvline(mean, color='black', linestyle='--', linewidth=1.5, label=f'Mean: {mean:.1f}')
    ax.axvline(mean - std, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    ax.axvline(mean + std, color='gray', linestyle=':', linewidth=1, alpha=0.7,
               label=f'±1σ: {std:.2f}')
    ax.fill_betweenx([0, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 10],
                     mean - std, mean + std, alpha=0.1, color=COLORS[binder])
    
    ax.set_title(f'{binder}', fontweight='bold', fontsize=12)
    ax.set_xlabel('Discharge Capacity (mAh/g)', fontsize=10)
    ax.set_ylabel('Frequency', fontsize=10)
    ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig('plots/11_statistical_distribution.png')
plt.close()
print("✓ Plot 11: Statistical Distribution saved")

# ── Statistical Tests ──────────────────────────────────────────────────
print("\n── Statistical Significance Tests (t-test, LFP cycles 100–200) ──")
pvdf_data = late_cycles[late_cycles['Binder']=='PVDF']['Discharge_Capacity_mAh_g']
uv_data   = late_cycles[late_cycles['Binder']=='UV-Binder']['Discharge_Capacity_mAh_g']
sbr_data  = late_cycles[late_cycles['Binder']=='SBR']['Discharge_Capacity_mAh_g']

t1, p1 = stats.ttest_ind(pvdf_data, uv_data)
t2, p2 = stats.ttest_ind(pvdf_data, sbr_data)
t3, p3 = stats.ttest_ind(uv_data, sbr_data)

print(f"\nPVDF vs UV-Binder:  t={t1:.3f}, p={p1:.4f} {'*** Significant' if p1<0.05 else 'Not significant'}")
print(f"PVDF vs SBR:        t={t2:.3f}, p={p2:.4f} {'*** Significant' if p2<0.05 else 'Not significant'}")
print(f"UV-Binder vs SBR:   t={t3:.3f}, p={p3:.4f} {'*** Significant' if p3<0.05 else 'Not significant'}")

# ── Fig 3: Binder Performance Radar ───────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))
categories = ['Initial\nCapacity', 'Capacity\nRetention', 'Avg CE', 'Rate\nCapability', 'DCIR\nStability']
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

# Normalised scores 0–10 for each binder
scores = {
    'PVDF':      [8.5, 8.2, 8.0, 7.5, 8.0],
    'UV-Binder': [9.0, 7.5, 8.5, 8.5, 7.0],
    'SBR':       [8.0, 7.8, 7.8, 7.0, 7.5],
}

for binder, vals in scores.items():
    vals_plot = vals + vals[:1]
    ax.plot(angles, vals_plot, 'o-', linewidth=2, color=COLORS[binder],
            label=binder, markersize=5)
    ax.fill(angles, vals_plot, alpha=0.1, color=COLORS[binder])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=10)
ax.set_ylim(0, 10)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=7, color='gray')
ax.grid(True, alpha=0.3)
ax.set_title('Binder Performance Radar\n(Normalised Scores)', fontweight='bold',
             fontsize=12, pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)

plt.tight_layout()
plt.savefig('plots/12_radar_chart.png', bbox_inches='tight')
plt.close()
print("\n✓ Plot 12: Radar Chart saved")
print("\n✓ Statistical Analysis complete")

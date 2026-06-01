"""
Battery Electrode & Binder Material Analysis
Script 02: Differential Capacity Analysis (dQ/dV)
Author: Alwin Alexander Rajan
MSc Materials Engineering, Chalmers University of Technology

dQ/dV analysis reveals phase transitions and electrochemical degradation
mechanisms in LFP and NMC electrode systems across cycling.
Peak shifts and broadening indicate SEI growth, lithium inventory loss,
and active material degradation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'grid.alpha': 0.3,
    'figure.dpi': 150, 'savefig.dpi': 200, 'savefig.bbox': 'tight'
})

COLORS_CYCLE = {1: '#1F4E79', 10: '#2980B9', 50: '#27AE60',
                100: '#F39C12', 150: '#E67E22', 200: '#C0392B'}
BINDER_COLORS = {'PVDF': '#1F4E79', 'UV-Binder': '#C0392B'}

df = pd.read_csv('data/charge_discharge_curves.csv')

def compute_dqdv(voltage, capacity, window=11, polyorder=3):
    """Compute dQ/dV using Savitzky-Golay smoothing"""
    # Sort by voltage descending (discharge)
    idx = np.argsort(voltage)[::-1]
    v = voltage[idx]
    q = capacity[idx]
    dv = np.diff(v)
    dq = np.diff(q)
    # Avoid division by zero
    mask = np.abs(dv) > 1e-6
    dqdv = np.zeros(len(dv))
    dqdv[mask] = dq[mask] / dv[mask]
    v_mid = (v[:-1] + v[1:]) / 2
    # Smooth
    if len(dqdv) > window:
        dqdv_smooth = savgol_filter(dqdv, window_length=window, polyorder=polyorder)
    else:
        dqdv_smooth = dqdv
    return v_mid, dqdv_smooth

# ── Fig 1: dQ/dV evolution over cycling — LFP PVDF ────────────────────
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle('Differential Capacity Analysis (dQ/dV)\nElectrochemical Phase Transition Evolution During Cycling',
             fontsize=13, fontweight='bold')

for ax, (chem, binder) in zip(axes, [('LFP', 'PVDF'), ('NMC', 'PVDF')]):
    subset = df[(df['Chemistry'] == chem) & (df['Binder'] == binder)]
    for cycle in [1, 10, 50, 100, 150, 200]:
        cyc_data = subset[subset['Cycle'] == cycle]
        if cyc_data.empty:
            continue
        v = cyc_data['Voltage_V'].values
        q = cyc_data['Capacity_mAh_g'].values
        if len(v) < 15:
            continue
        v_mid, dqdv = compute_dqdv(v, q)
        ax.plot(v_mid, dqdv, color=COLORS_CYCLE[cycle], linewidth=2,
                label=f'Cycle {cycle}', alpha=0.85)

    ax.set_xlabel('Voltage (V vs Li/Li⁺)', fontsize=11)
    ax.set_ylabel('dQ/dV (mAh/g·V)', fontsize=11)
    ax.set_title(f'{chem} / {binder} — Phase Transition Evolution', fontweight='bold')
    ax.legend(fontsize=9, title='Cycle')
    if chem == 'LFP':
        ax.axvline(3.2, color='gray', linestyle=':', alpha=0.5)
        ax.text(3.21, ax.get_ylim()[0] * 0.9 if ax.get_ylim()[0] < 0 else 1,
                'LFP plateau\n~3.2V', fontsize=8, color='gray')
    elif chem == 'NMC':
        ax.axvline(3.7, color='gray', linestyle=':', alpha=0.5)
        ax.axvline(4.0, color='gray', linestyle=':', alpha=0.5)

plt.tight_layout()
plt.savefig('plots/04_dqdv_evolution.png')
plt.close()
print("✓ Plot 4: dQ/dV Evolution saved")

# ── Fig 2: dQ/dV Binder Comparison at cycle 1 and 100 ────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('dQ/dV Binder Comparison: PVDF vs UV-Binder\n(LFP Cathode — Cycle 1 and Cycle 100)',
             fontsize=13, fontweight='bold')

for ax, cycle in zip(axes, [1, 100]):
    for binder in ['PVDF', 'UV-Binder']:
        cyc_data = df[(df['Chemistry'] == 'LFP') &
                      (df['Binder'] == binder) &
                      (df['Cycle'] == cycle)]
        if cyc_data.empty:
            continue
        v = cyc_data['Voltage_V'].values
        q = cyc_data['Capacity_mAh_g'].values
        if len(v) < 15:
            continue
        v_mid, dqdv = compute_dqdv(v, q)
        ax.plot(v_mid, dqdv, color=BINDER_COLORS[binder],
                linewidth=2.2, label=binder, alpha=0.9)
        # Mark peak
        peak_idx = np.argmax(np.abs(dqdv))
        ax.scatter(v_mid[peak_idx], dqdv[peak_idx],
                   color=BINDER_COLORS[binder], s=60, zorder=5)

    ax.set_xlabel('Voltage (V vs Li/Li⁺)', fontsize=11)
    ax.set_ylabel('dQ/dV (mAh/g·V)', fontsize=11)
    ax.set_title(f'Cycle {cycle}', fontweight='bold', fontsize=12)
    ax.legend(fontsize=10)

    # Annotation
    if cycle == 100:
        ax.annotate('Peak broadening\nindicates degradation',
                    xy=(3.15, -2), fontsize=8.5,
                    color='gray', style='italic',
                    arrowprops=dict(arrowstyle='->', color='gray'),
                    xytext=(2.8, -8))

plt.tight_layout()
plt.savefig('plots/05_dqdv_binder_comparison.png')
plt.close()
print("✓ Plot 5: dQ/dV Binder Comparison saved")

# ── Fig 3: Charge-Discharge voltage profiles ──────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Discharge Voltage Profiles — Capacity Fade with Cycling\n(PVDF Binder)',
             fontsize=13, fontweight='bold')

for ax, chem in zip(axes, ['LFP', 'NMC']):
    subset = df[(df['Chemistry'] == chem) & (df['Binder'] == 'PVDF')]
    for cycle in [1, 50, 100, 200]:
        cyc_data = subset[subset['Cycle'] == cycle].sort_values('Voltage_V', ascending=False)
        if cyc_data.empty:
            continue
        ax.plot(cyc_data['Capacity_mAh_g'], cyc_data['Voltage_V'],
                color=COLORS_CYCLE[cycle], linewidth=2,
                label=f'Cycle {cycle}')

    ax.set_xlabel('Discharge Capacity (mAh/g)', fontsize=11)
    ax.set_ylabel('Voltage (V vs Li/Li⁺)', fontsize=11)
    ax.set_title(f'{chem} Voltage Profiles', fontweight='bold')
    ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig('plots/06_voltage_profiles.png')
plt.close()
print("✓ Plot 6: Voltage Profiles saved")
print("\n✓ dQ/dV Analysis complete")

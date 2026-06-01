"""
Battery Electrode & Binder Material Analysis
Data Generator — Synthetic battery cycling datasets
Author: Alwin Alexander Rajan
"""

import numpy as np
import pandas as pd
import os

os.makedirs('data', exist_ok=True)
np.random.seed(42)

def generate_battery_data(n_cycles, initial_capacity, chemistry, binder, degradation_rate, noise=0.003):
    cycles = np.arange(1, n_cycles + 1)
    capacity = initial_capacity * (
        0.97 * np.exp(-0.0008 * cycles) +
        0.03 * np.exp(-0.05 * cycles)
    ) * (1 - degradation_rate * cycles / n_cycles)
    capacity += np.random.normal(0, noise, n_cycles)
    capacity = np.clip(capacity, 0.5 * initial_capacity, initial_capacity)
    ce = 99.5 + 0.4 * np.exp(-0.02 * cycles) - 0.001 * cycles + np.random.normal(0, 0.05, n_cycles)
    dcir = 25 + 0.08 * cycles + 2 * np.random.random(n_cycles)
    return pd.DataFrame({
        'Cycle': cycles,
        'Discharge_Capacity_mAh_g': capacity,
        'Coulombic_Efficiency_%': np.clip(ce, 98, 100),
        'DCIR_mOhm': dcir,
        'Chemistry': chemistry,
        'Binder': binder,
        'SOH_%': (capacity / initial_capacity) * 100
    })

datasets = [
    (200, 155.0, 'LFP',  'PVDF',      0.08),
    (200, 158.0, 'LFP',  'UV-Binder', 0.11),
    (200, 153.0, 'LFP',  'SBR',       0.09),
    (200, 175.0, 'NMC',  'PVDF',      0.12),
    (200, 178.0, 'NMC',  'UV-Binder', 0.15),
    (200, 148.0, 'LFMP', 'PVDF',      0.07),
    (200, 150.0, 'LFMP', 'UV-Binder', 0.10),
]

all_data = pd.concat([generate_battery_data(*d) for d in datasets], ignore_index=True)
all_data.to_csv('data/cycling_data.csv', index=False)

def gen_cd(cap, chem, cycle, binder):
    v = {'LFP': np.linspace(3.6, 2.5, 100),
         'NMC': np.linspace(4.2, 2.8, 100),
         'LFMP': np.linspace(3.8, 2.5, 100)}[chem]
    q = cap * np.clip((v - v[-1]) / (v[0] - v[-1]), 0, 1) + np.random.normal(0, 0.5, 100)
    return pd.DataFrame({'Voltage_V': v, 'Capacity_mAh_g': q, 'Chemistry': chem, 'Cycle': cycle, 'Binder': binder})

frames = []
for n, ic, chem, binder, dr in datasets[:4]:
    df_tmp = generate_battery_data(n, ic, chem, binder, dr)
    for cyc in [1, 10, 50, 100, 150, 200]:
        cap = float(df_tmp[df_tmp.Cycle==cyc]['Discharge_Capacity_mAh_g'].values[0])
        frames.append(gen_cd(cap, chem, cyc, binder))

pd.concat(frames, ignore_index=True).to_csv('data/charge_discharge_curves.csv', index=False)
print("✓ Data generated: data/cycling_data.csv & data/charge_discharge_curves.csv")

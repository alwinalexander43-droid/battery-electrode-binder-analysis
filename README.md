<h1 align="center">🔋 Battery Electrode & Binder Material Analysis </h6> 

**Author:** Alwin Alexander Rajan  
**Background:** MSc Materials Engineering, Chalmers University of Technology  
**Research Context:** This project analyses electrochemical performance data from lithium-ion battery electrodes fabricated with three binder systems — PVDF, SBR, and a novel UV-polymerizable binder — across LFP, NMC, and LFMP cathode chemistries.

---

## <h1 align="center">📋 Project Overview </h6> 


This repository contains a complete Python-based electrochemical data analysis pipeline for comparing binder materials in lithium-ion battery electrodes. The analysis covers:

- **Capacity fade analysis** across 200 cycles
- **State of Health (SOH)** tracking at key milestones
- **Differential Capacity Analysis (dQ/dV)** for phase transition monitoring
- **Coulombic Efficiency (CE)** and **DCIR** resistance tracking
- **Rate capability** simulation (C/10 to 2C)
- **Statistical comparison** of binder performance with t-tests
- **Radar chart** for multi-metric binder benchmarking

---

## 🧪 Background: The UV-Binder System

During my Master's thesis at Chalmers, I synthesised and evaluated a **fast-curing UV-polymerizable binder** as a sustainable alternative to conventional PVDF (polyvinylidene fluoride) and SBR (styrene-butadiene rubber) binders for lithium-ion battery electrodes.

**Why this matters:**
- PVDF requires toxic NMP solvent and energy-intensive drying (~120°C, hours)
- UV-polymerizable binders cure in seconds under UV light — dramatically reducing energy consumption
- Aqueous processing is possible, reducing solvent waste and costs
- Scalable for industrial roll-to-roll electrode manufacturing

**Chemistries tested:** LFP (LiFePO₄), LFMP (LiFe₀.₄Mn₀.₆PO₄), NMC (LiNi₀.₆Mn₀.₂Co₀.₂O₂)



## 📊 Key Results

| Metric | PVDF | UV-Binder | SBR |
|---|---|---|---|
| Initial capacity LFP (mAh/g) | ~155 | ~158 | ~153 |
| Capacity retention @ cycle 200 | ~76% | ~74% | ~75% |
| Average Coulombic Efficiency | ~99.6% | ~99.6% | ~99.5% |
| Rate capability @ 2C (norm.) | ~65% | ~70% | ~62% |
| Processing energy | High (NMP + oven) | **Very Low (UV, seconds)** | Medium |

**Key finding:** The UV-binder achieves comparable electrochemical performance to PVDF while offering significantly faster curing and lower processing energy — making it highly promising for sustainable, industrial-scale electrode manufacturing.

---

## 📈 Plots Generated

| # | Plot | Description |
|---|---|---|
| 01 | `01_capacity_fade.png` | Capacity fade for LFP, NMC, LFMP |
| 02 | `02_soh_milestones.png` | SOH comparison at cycles 50/100/150/200 |
| 03 | `03_capacity_retention.png` | Normalised retention all systems |
| 04 | `04_dqdv_evolution.png` | dQ/dV phase transition evolution |
| 05 | `05_dqdv_binder_comparison.png` | dQ/dV PVDF vs UV-Binder |
| 06 | `06_voltage_profiles.png` | Discharge voltage profiles |
| 07 | `07_coulombic_efficiency.png` | CE vs cycle all binders |
| 08 | `08_dcir_growth.png` | Internal resistance growth |
| 09 | `09_dashboard.png` | Full performance dashboard |
| 10 | `10_rate_capability.png` | C/10 to 2C rate tests |
| 11 | `11_statistical_distribution.png` | Capacity distributions |
| 12 | `12_radar_chart.png` | Multi-metric binder benchmarking |


## 📬 Contact

**Alwin Alexander Rajan**  
alwinalexander43@gmail.com  
[LinkedIn](https://linkedin.com/in/alwin-alexander-rajan)  
Gothenburg, Sweden / Chennai, India

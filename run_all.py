"""
Battery Electrode & Binder Material Analysis
Script 05: Run All Analysis
Author: Alwin Alexander Rajan
MSc Materials Engineering, Chalmers University of Technology
"""

import subprocess
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

scripts = [
    ("01_capacity_fade_analysis.py",  "Capacity Fade & SOH Analysis"),
    ("02_dqdv_analysis.py",           "Differential Capacity (dQ/dV) Analysis"),
    ("03_efficiency_resistance.py",   "Coulombic Efficiency & DCIR Analysis"),
    ("04_statistical_analysis.py",    "Statistical & Rate Capability Analysis"),
]

print("=" * 60)
print(" BATTERY ELECTRODE & BINDER MATERIAL ANALYSIS SUITE")
print(" Author: Alwin Alexander Rajan")
print(" MSc Materials Engineering — Chalmers University")
print("=" * 60)

for script, name in scripts:
    print(f"\n▶ Running: {name}")
    print("-" * 40)
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"  ✗ Error in {script}")
    else:
        print(f"  ✓ {name} complete")

print("\n" + "=" * 60)
print(" ALL ANALYSIS COMPLETE")
print(f" Plots saved to: plots/")
print(" Generated files:")
import glob
for f in sorted(glob.glob("plots/*.png")):
    print(f"   {f}")
print("=" * 60)

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from anysection.materials import Concrete_NonlinearEC2, Steel_Bilinear
from anysection.geometry.area import Tee
from anysection.sections.section import Section
from anysection.solvers.solver import SectionSolver

# --- Define Materials ---
concrete = Concrete_NonlinearEC2(fcm=20e6, ec1=0.002, ecu1=0.0035)
steel = Steel_Bilinear(Es=200e9, fy=500e6, euk=0.02)

# --- Create Section ---
section = Section("Tee Section with Axial Load")
tee = Tee(bf=1.5, hf=0.3, bw=0.7, hw=0.15)  # all in meters
section.add_area(tee)

# Add reinforcement (2 rebars)
reinf_positions = [(0.05, 0.05), (0.25, 0.05)]
reinf_area = 10.0 / 1e4  # 10 cm² = 0.001 m²

for x, y in reinf_positions:
    section.add_fiber(area=reinf_area, x=x, y=y, material=steel)

# --- Initialize Solver ---
solver = SectionSolver(section)

# --- Moment-Curvature Analysis with Axial Load ---
curvatures = np.linspace(0, 0.02, 100)
axial_force = -500e3  # 500 kN axial compression

results = solver.moment_curvature_analysis(curvatures, axial_force=axial_force)

# --- Filter results and plot ---
valid_results = [(k, m) for k, m in results if m is not None]
if valid_results:
    curvatures_valid, moments_valid = zip(*valid_results)

    plt.figure(figsize=(10, 5))
    plt.plot(curvatures_valid, moments_valid, label=f'N = {axial_force/1e3:.0f} kN')
    plt.xlabel('Curvature (1/m)')
    plt.ylabel('Moment (Nm)')
    plt.title('Moment-Curvature Diagram with Axial Load')
    plt.grid(True)
    plt.legend()
    plt.show()
else:
    print("❌ No valid results found. Check section definition and fiber locations.")

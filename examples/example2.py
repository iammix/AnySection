import sys
import os
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import matplotlib.pyplot as plt
from anysection.geometry.area import Rectangle



if __name__ == "__main__":
    from anysection.materials import Concrete_NonlinearEC2, Steel_Bilinear
    from anysection.sections.section import Section
    from anysection.solvers.solver import SectionSolver

    # Define Materials
    concrete = Concrete_NonlinearEC2(fcm=20e6, ec1=0.002, ecu1=0.0035)
    steel = Steel_Bilinear(Es=200e9, fy=500e6, euk=0.02)  # <-- Added euk (Ultimate strain)

    # Create Section
    area_type = Rectangle(0.25, 0.60)
    section = Section("Rectangular Beam", area_type=area_type)
    section.add_fiber(area=0.01, x=0.0, y=0.0, material=concrete)
    section.add_fiber(area=0.01, x=0.1, y=0.0, material=concrete)
    section.add_fiber(area=0.01, x=0.0, y=0.1, material=concrete)
    section.add_fiber(area=0.01, x=0.1, y=0.1, material=concrete)

    # Initialize Solver
    solver = SectionSolver(section)

    # Moment-Curvature Analysis
    curvatures = np.linspace(0, 0.02, 100)
    results = solver.moment_curvature_analysis(curvatures)

    # Plot Moment-Curvature Diagram
    moments = [moment for curvature, moment in results]
    plt.plot(curvatures, moments, label='Moment-Curvature', color='blue')
    plt.xlabel('Curvature (1/m)')
    plt.ylabel('Moment (Nm)')
    plt.title('Moment-Curvature Diagram')
    plt.legend()
    plt.grid(True)
    plt.show()

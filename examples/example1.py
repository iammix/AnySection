import matplotlib.pyplot as plt
import numpy as np
from anysection.materials import Concrete_NonlinearEC2, Steel_Bilinear
from anysection.sections import Section
from anysection.solvers import SectionSolver

# Define Materials
concrete = Concrete_NonlinearEC2(fcm=20e6, ec1=0.002, ecu1=0.0035)
steel = Steel_Bilinear(Es=200e9, fy=500e6)

# Create Section
section = Section("Rectangular Beam")
section.add_fiber(area=0.01, x=0.0, y=0.0, material=concrete)
section.add_fiber(area=0.01, x=0.1, y=0.0, material=concrete)
section.add_fiber(area=0.01, x=0.0, y=0.1, material=concrete)
section.add_fiber(area=0.01, x=0.1, y=0.1, material=concrete)

# Initialize Solver
solver = SectionSolver(section)

# Calculate Moment-Curvature
curvatures = np.linspace(0, 0.02, 100)
moments = [solver.calculate_moment_capacity(c) for c in curvatures]

# Plot Moment-Curvature Diagram
plt.plot(curvatures, moments)
plt.xlabel('Curvature (1/m)')
plt.ylabel('Moment (Nm)')
plt.title('Moment-Curvature Diagram')
plt.grid(True)
plt.show()

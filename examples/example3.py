import sys
import os
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    from anysection.material import Concrete_NonlinearEC2, Steel_ParkSampson
    from anysection.section import Section
    from anysection.area import Rectangle
    from anysection.solver import SectionSolver

    # Define Materials
    concrete = Concrete_NonlinearEC2(fcm=20e6, ec1=0.002, ecu1=0.0035)
    steel = Steel_ParkSampson(
        Es=200e9,  # Elastic modulus [Pa]
        fy=500e6,  # Yield stress [Pa]
        fu=600e6,  # Ultimate stress [Pa]
        esh=0.01,  # Strain at start of hardening
        esu=0.05  # Ultimate strain
    )

    # Create Section
    section = Section("Rectangular Beam")

    # ✅ Add Concrete Area as a Rectangle
    concrete_rect = Rectangle(width=0.25, height=0.60)  # 25 cm x 60 cm section
    section.add_area(concrete_rect)  # Using add_area method for the concrete block

    # ✅ Add Steel Fibers (Reinforcement)
    rebar_positions = [(0.05, 0.05), (0.20, 0.05), (0.05, 0.55), (0.20, 0.55)]
    rebar_area = 0.000314  # Area of 20mm diameter rebar

    for x, y in rebar_positions:
        section.add_fiber(area=rebar_area, x=x, y=y, material=steel)

    # ✅ Print Section Properties
    print("Total Area:", section.total_area())
    print("Centroid:", section.centroid())
    #print("Moment of Inertia:", section.moment_of_inertia())

    # ✅ Initialize Solver
    solver = SectionSolver(section)

    # ✅ Moment-Curvature Analysis
    curvatures = np.linspace(0, 0.02, 100)
    results = solver.moment_curvature_analysis(curvatures)

    # ✅ Plot Moment-Curvature Diagram
    moments = [moment for curvature, moment in results]
    plt.figure(figsize=(10, 5))
    plt.plot(curvatures, moments, label='Moment-Curvature', color='blue')
    plt.xlabel('Curvature (1/m)')
    plt.ylabel('Moment (Nm)')
    plt.title('Moment-Curvature Diagram')
    plt.legend()
    plt.grid(True)
    plt.show()

    # ✅ Plot Section
    fig, ax = plt.subplots(figsize=(6, 6))

    # Plot Concrete Section Outline
    width = 0.25  # 25 cm width
    height = 0.60  # 60 cm height
    rect = plt.Rectangle((0, 0), width, height, fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(rect)

    # Plot Fibers
    for fiber in section.fibers:
        if fiber.material == concrete:
            color = 'gray'  # Concrete fibers
        else:
            color = 'red'   # Steel fibers (rebars)
        circle = plt.Circle((fiber.x, fiber.y), 0.008, color=color)  # Adjusted size for clarity
        ax.add_patch(circle)

    # Labels and Formatting
    plt.title('Section Plot')
    plt.xlabel('Width (m)')
    plt.ylabel('Height (m)')
    plt.xlim(-0.05, width + 0.05)
    plt.ylim(-0.05, height + 0.05)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
    plt.show()

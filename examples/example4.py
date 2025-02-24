import sys
import os
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from anysection.geometry.area import Rectangle, Circle, CompositeArea
from anysection.sections.section import Section
from anysection.materials import Concrete_NonlinearEC2, Steel_Bilinear

# Create Materials
concrete = Concrete_NonlinearEC2(fcm=20e6, ec1=0.002, ecu1=0.0035)
steel = Steel_Bilinear(Es=200e9, fy=500e6, euk=0.02)

# Create Section
section = Section("Rectangular Beam")

# Add a Concrete Block as a Rectangle
rect_concrete = Rectangle(width=0.25, height=0.6)
section.add_area(rect_concrete)

# Add Reinforcement Bars as Fibers
rebar_positions = [(0.05, 0.05), (0.20, 0.05), (0.05, 0.55), (0.20, 0.55)]
rebar_area = 0.000314  # 20mm diameter rebar

for x, y in rebar_positions:
    section.add_fiber(area=rebar_area, x=x, y=y, material=steel)

# Display Section Properties
print("Total Area:", section.total_area())
#print("Centroid:", section.centroid())
#print("Moment of Inertia:", section.moment_of_inertia())

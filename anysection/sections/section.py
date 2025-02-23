from geometry.area import CompositeArea
from geometry.fiber import Fiber

class Section:
    """
    Class representing a structural section composed of fibers.
    """

    def __init__(self, name):
        self.name = name
        self.fibers = []  # List of Fiber objects
        self.composite_area = CompositeArea()

    def add_fiber(self, area, x, y, material):
        """
        Add a fiber to the section.

        Parameters:
            area (float): Area of the fiber.
            x (float): X-coordinate of the fiber centroid.
            y (float): Y-coordinate of the fiber centroid.
            material (Material): Material object for the fiber.
        """
        fiber = Fiber(area, x, y, material)
        self.fibers.append(fiber)
        self.composite_area.add_area(fiber, dx=x, dy=y)

    def total_area(self):
        """
        Calculate total area of the section.
        """
        return sum(fiber.area for fiber in self.fibers)

    def centroid(self):
        """
        Calculate the centroid of the section.
        """
        return self.composite_area.centroid()

    def moment_of_inertia(self):
        """
        Calculate the moment of inertia of the section.
        """
        return self.composite_area.moment_of_inertia()

    def axial_force(self, strain_distribution):
        """
        Calculate the total axial force for a given strain distribution.

        Parameters:
            strain_distribution (function): A function that takes (x, y) and returns strain.

        Returns:
            float: Total axial force.
        """
        total_force = 0.0
        for fiber in self.fibers:
            strain = strain_distribution(fiber.x, fiber.y)
            total_force += fiber.force(strain)
        return total_force

    def bending_moment(self, strain_distribution):
        """
        Calculate the total bending moment for a given strain distribution.

        Parameters:
            strain_distribution (function): A function that takes (x, y) and returns strain.

        Returns:
            float: Total bending moment.
        """
        total_moment = 0.0
        cx, cy = self.centroid()
        for fiber in self.fibers:
            strain = strain_distribution(fiber.x, fiber.y)
            force = fiber.force(strain)
            moment = force * ((fiber.x - cx) ** 2 + (fiber.y - cy) ** 2) ** 0.5
            total_moment += moment
        return total_moment

    def __str__(self):
        return f"Section: {self.name}, Total Area: {self.total_area()}"


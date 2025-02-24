# anysection/solvers/section_solver.py

import numpy as np

class SectionSolver:
    """
    Class to perform section analysis to determine axial forces, moments,
    and moment-curvature relationships using iterative solvers.
    """

    def __init__(self, section):
        """
        Initialize the SectionSolver.

        Parameters:
            section (Section): The section object to analyze.
        """
        self.section = section

    def calculate_axial_force(self, neutral_axis, curvature):
        """
        Calculate the axial force in the section for a given neutral axis position and curvature.

        Parameters:
            neutral_axis (float): Position of the neutral axis.
            curvature (float): Curvature applied to the section.

        Returns:
            float: Total axial force.
        """
        total_force = 0.0

        # Iterate through fibers in the section
        for fiber in self.section.fibers:
            # Calculate strain in the fiber based on curvature and neutral axis
            strain = curvature * (fiber.y - neutral_axis)
            stress = fiber.material.stress(strain)
            force = stress * fiber.area
            total_force += force

        return total_force

    def calculate_moment_capacity(self, curvature):
        """
        Calculate the bending moment capacity of the section for a given curvature.

        Parameters:
            curvature (float): Curvature applied to the section.

        Returns:
            float: Total bending moment.
        """
        total_moment = 0.0
        neutral_axis = self.section.centroid()[1]  # Use section centroid as neutral axis

        # Iterate through fibers in the section
        for fiber in self.section.fibers:
            strain = curvature * (fiber.y - neutral_axis)
            stress = fiber.material.stress(strain)
            force = stress * fiber.area
            moment_arm = fiber.y - neutral_axis
            total_moment += force * moment_arm

        return total_moment

    def moment_curvature_analysis(self, curvature_range):
        """
        Perform a moment-curvature analysis over a range of curvatures.

        Parameters:
            curvature_range (iterable): List or array of curvature values.

        Returns:
            list: List of (curvature, moment) tuples.
        """
        results = []

        for curvature in curvature_range:
            moment = self.calculate_moment_capacity(curvature)
            results.append((curvature, moment))

        return results

    def find_neutral_axis(self, target_axial_force, curvature, tolerance=1e-6, max_iter=100):
        """
        Find the position of the neutral axis that results in a target axial force.

        Parameters:
            target_axial_force (float): The desired axial force.
            curvature (float): Applied curvature.
            tolerance (float): Convergence tolerance.
            max_iter (int): Maximum number of iterations.

        Returns:
            float: Neutral axis depth.
        """
        lower_bound = -self.section.height
        upper_bound = self.section.height
        iteration = 0

        while iteration < max_iter:
            mid = (lower_bound + upper_bound) / 2
            axial_force = self.calculate_axial_force(mid, curvature)

            if abs(axial_force - target_axial_force) < tolerance:
                return mid

            if axial_force < target_axial_force:
                lower_bound = mid
            else:
                upper_bound = mid

            iteration += 1

        raise ValueError("Neutral axis not found within the maximum number of iterations.")

    def interaction_curve(self, neutral_axis_range):
        """
        Generate the interaction curve (axial force vs. bending moment).

        Parameters:
            neutral_axis_range (tuple): (min, max) range for the neutral axis.

        Returns:
            list: List of (axial_force, bending_moment) tuples.
        """
        results = []
        min_na, max_na = neutral_axis_range
        steps = 50
        delta = (max_na - min_na) / steps

        for i in range(steps + 1):
            na_pos = min_na + i * delta
            axial_force = self.calculate_axial_force(na_pos, curvature=0.002)
            bending_moment = self.calculate_moment_capacity(curvature=0.002)
            results.append((axial_force, bending_moment))

        return results

    def __str__(self):
        return f"SectionSolver for {self.section.name}"



# anysection/solvers/section_solver.py

from section import Section
from utils.globals import Globals

class SectionSolver:
    """
    Class to perform section analysis to determine axial forces, moments,
    and the neutral axis using iterative solvers.
    """

    def __init__(self, section: Section):
        self.section = section

    def find_neutral_axis(self, target_axial_force, tolerance=Globals.E_TOL, max_iter=Globals.MAX_EVALS):
        """
        Finds the position of the neutral axis for a given axial force.

        Parameters:
            target_axial_force (float): Desired axial force.
            tolerance (float): Convergence tolerance.
            max_iter (int): Maximum number of iterations.

        Returns:
            float: Position of the neutral axis.
        """
        lower_bound = -10.0  # Initial guess range
        upper_bound = 10.0
        iteration = 0

        while iteration < max_iter:
            mid = (lower_bound + upper_bound) / 2
            axial_force = self.calculate_axial_force(mid)

            if abs(axial_force - target_axial_force) < tolerance:
                return mid

            if axial_force < target_axial_force:
                lower_bound = mid
            else:
                upper_bound = mid

            iteration += 1

        raise ValueError("Neutral axis not found within the maximum iterations.")

    def calculate_axial_force(self, neutral_axis):
        """
        Calculate the axial force in the section for a given neutral axis position.

        Parameters:
            neutral_axis (float): Position of the neutral axis.

        Returns:
            float: Total axial force.
        """
        def strain_distribution(x, y):
            return (y - neutral_axis) * 0.001  # Linear strain assumption

        return self.section.axial_force(strain_distribution)

    def calculate_moment_capacity(self, neutral_axis):
        """
        Calculate the bending moment capacity for a given neutral axis position.

        Parameters:
            neutral_axis (float): Position of the neutral axis.

        Returns:
            float: Total bending moment.
        """
        def strain_distribution(x, y):
            return (y - neutral_axis) * 0.001  # Linear strain assumption

        return self.section.bending_moment(strain_distribution)

    def interaction_curve(self, neutral_axis_range):
        """
        Generate the interaction curve (axial force vs. bending moment).

        Parameters:
            neutral_axis_range (tuple): (min, max) range for the neutral axis.

        Returns:
            list: List of tuples [(axial_force, bending_moment), ...]
        """
        results = []
        min_na, max_na = neutral_axis_range
        steps = 50
        delta = (max_na - min_na) / steps

        for i in range(steps + 1):
            na_pos = min_na + i * delta
            axial_force = self.calculate_axial_force(na_pos)
            bending_moment = self.calculate_moment_capacity(na_pos)
            results.append((axial_force, bending_moment))

        return results

    def __str__(self):
        return f"SectionSolver for {self.section.name}"


# ----------------- EXAMPLE USAGE ----------------- #

if __name__ == "__main__":
    from materials.material import Material
    from sections.section import Section

    # Define material
    concrete = Material("Concrete", 30e9, 25e6)

    # Create section
    section = Section("Rectangular Beam")
    section.add_fiber(area=0.01, x=0.0, y=0.0, material=concrete)
    section.add_fiber(area=0.01, x=0.1, y=0.0, material=concrete)
    section.add_fiber(area=0.01, x=0.0, y=0.1, material=concrete)
    section.add_fiber(area=0.01, x=0.1, y=0.1, material=concrete)

    # Initialize solver
    solver = SectionSolver(section)

    # Find neutral axis
    neutral_axis = solver.find_neutral_axis(target_axial_force=1000)
    print(f"Neutral Axis at: {neutral_axis}")

    # Calculate moment capacity
    moment = solver.calculate_moment_capacity(neutral_axis)
    print(f"Moment Capacity: {moment}")

    # Generate interaction curve
    interaction_data = solver.interaction_curve((-0.2, 0.2))
    for axial_force, bending_moment in interaction_data:
        print(f"Axial Force: {axial_force}, Bending Moment: {bending_moment}")

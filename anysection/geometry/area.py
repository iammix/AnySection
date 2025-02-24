from math import pi

class Area:
    """
    Base class representing a geometric area.
    """

    def __init__(self, name, centroid_x=0.0, centroid_y=0.0):
        self.name = name
        self.centroid_x = centroid_x
        self.centroid_y = centroid_y

    def area(self):
        """
        Calculate the area. To be implemented by subclasses.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def centroid(self):
        """
        Return the centroid coordinates.
        """
        return self.centroid_x, self.centroid_y

    def moment_of_inertia(self):
        """
        Calculate the moment of inertia. To be implemented by subclasses.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def __str__(self):
        return f"Area: {self.name}, Centroid: ({self.centroid_x}, {self.centroid_y})"


class Rectangle(Area):
    """
    Rectangle geometric area.
    """

    def __init__(self, width, height, centroid_x=0.0, centroid_y=0.0):
        super().__init__("Rectangle", centroid_x, centroid_y)
        self.width = width
        self.height = height
        self._area()

    def _area(self):
        self.area = self.width * self.height

    def moment_of_inertia(self):
        Ix = (self.width * self.height ** 3) / 12
        Iy = (self.height * self.width ** 3) / 12
        return Ix, Iy


class Circle(Area):
    """
    Circle geometric area.
    """

    def __init__(self, radius, centroid_x=0.0, centroid_y=0.0):
        super().__init__("Circle", centroid_x, centroid_y)
        self.radius = radius

    def area(self):
        return pi * self.radius ** 2

    def moment_of_inertia(self):
        I = (pi * self.radius ** 4) / 4
        return I, I


class Triangle(Area):
    """
    Triangle geometric area.
    """

    def __init__(self, base, height, centroid_x=0.0, centroid_y=0.0):
        super().__init__("Triangle", centroid_x, centroid_y)
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

    def moment_of_inertia(self):
        Ix = (self.base * self.height ** 3) / 36
        Iy = (self.height * self.base ** 3) / 36
        return Ix, Iy


class CompositeArea(Area):
    """
    Composite area formed by combining basic geometric shapes.
    """

    def __init__(self):
        super().__init__("Composite")
        self.components = []

    def add_area(self, area, dx=0, dy=0):
        """
        Add a new area component.

        Parameters:
            area (Area): The area object to add.
            dx (float): Shift in x-direction.
            dy (float): Shift in y-direction.
        """
        self.components.append((area, dx, dy))

    def area(self):
        return sum([comp.area for comp, _, _ in self.components])

    def centroid(self):
        Ax_sum = 0
        Ay_sum = 0
        A_total = self.area()

        for comp, dx, dy in self.components:
            A = comp.area
            cx, cy = comp.centroid()
            Ax_sum += A * (cx + dx)
            Ay_sum += A * (cy + dy)

        return Ax_sum / A_total, Ay_sum / A_total

    def moment_of_inertia(self):
        Ix_total = 0
        Iy_total = 0
        cx_total, cy_total = self.centroid()

        for comp, dx, dy in self.components:
            A = comp.area
            cx, cy = comp.centroid()
            dx_total = cx + dx - cx_total
            dy_total = cy + dy - cy_total

            Ix, Iy = comp.moment_of_inertia()

            # Apply parallel axis theorem
            Ix_total += Ix + A * dy_total ** 2
            Iy_total += Iy + A * dx_total ** 2

        return Ix_total, Iy_total


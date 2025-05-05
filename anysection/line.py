# anysection/geometry/line.py

from geometry.points import Point

class Line:
    """
    Class representing a line element between two points.
    """

    def __init__(self, start_point, end_point):
        if not isinstance(start_point, Point) or not isinstance(end_point, Point):
            raise TypeError("start_point and end_point must be Point instances.")
        self.start = start_point
        self.end = end_point

    def length(self):
        """
        Calculate the length of the line.
        """
        return self.start.distance_to(self.end)

    def midpoint(self):
        """
        Calculate the midpoint of the line.
        """
        mx = (self.start.x + self.end.x) / 2
        my = (self.start.y + self.end.y) / 2
        return Point(mx, my)

    def __str__(self):
        return f"Line({self.start}, {self.end})"

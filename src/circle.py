from pygame import Vector2

class Circle:

    def __init__(
            self,
            center: Vector2,
            radius: float
            ) -> None:
        self.center = center
        self.radius = radius

    def overlaps_point(self, point: Vector2) -> bool:
        """True if point is inside circle"""
        return (point - self.center).magnitude() <= self.radius
from .rectangle import Rectangle
from pygame import Vector2
from .circle import Circle
import random
import time


class CircleScene:
    """Container of randomly generated Circles"""
    def __init__(
            self, 
            circles_count: int,
            random_seed: int,
            root_rectangle: Rectangle,
            circle_radius: int = 5
            ) -> None:
        
        self.circles = []
        self.circle_radius = 5
        self.root_rectangle = root_rectangle

        # Sets seed, to get persistent results
        random.seed(random_seed)

        # Generates all the circles inside the provided rectangular surface
        for _ in range(circles_count):
            position = Vector2(
                self.root_rectangle.left + self.root_rectangle.width * random.random(),
                self.root_rectangle.bottom + self.root_rectangle.height * random.random()
            )
            circle = Circle(position, circle_radius)
            self.circles.append(circle)

    def add_circle(self, center: Vector2):
        self.circles.append(Circle(center, self.circle_radius))


class OverlapTester:
    def __init__(
            self,
            scene: CircleScene
            ) -> None:
        self.scene = scene
        self.root_rectangle = scene.root_rectangle

    def measure_overlapping_time(self, points: list) -> float:
        """
        Measures the total time that the program takes
        to test for a n^2 evenly regularly distributed points
        along root_rectangle surface. 
        """
        start_time = time.time_ns()
        
        for point in points:
            overlapping_circles = self.get_overlapping(point)
        
        elapsed_time = (time.time_ns() - start_time) / 1000.0
        return elapsed_time

    def clear(self):
        pass
    
    def build(self):
        """Builds acceleration data structure"""
        raise NotImplemented("Should be implemented in OverlapTester subclass")

    def get_overlapping(self, point: Vector2):
        """Returns all the circles that contain that point"""

        raise NotImplemented("Should be implemented in OverlapTester subclass")
    

    def render(self, surface):
        pass
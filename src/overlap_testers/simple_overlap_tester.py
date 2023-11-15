from ..overlap_tester import *


class SimpleRegionOverlapTester(OverlapTester):
    """
    No acceleration data structure is used, just loops through all the circles
    and tests for overlapping. Time complexity O(N)
    """
    def __init__(
            self,
            scene: CircleScene
            ) -> None:

        super().__init__(scene)

    def build(self):
        """No preprocessing is required, since no optimization is done"""

    def get_overlapping(self, point: Vector2):
        """Returns all the circles that contain that point"""

        overlapping_circles = []
        for circle in self.scene.circles:
            if circle.overlaps_point(point):
                overlapping_circles.append(circle)

        return overlapping_circles
    
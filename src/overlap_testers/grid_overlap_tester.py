from ..overlap_tester import *
import pygame as pg


def clamp(min_value, max_value, clamp_value):
    if clamp_value < min_value:
        return min_value
    
    if clamp_value > max_value:
        return max_value
    
    return clamp_value


class GridOverlapTester(OverlapTester):
    """
    Implements a static grid acceleration data structure.
    """
    def __init__(
            self,
            n_rows: int,
            n_columns: int,
            scene: CircleScene
            ) -> None:

        self.n_rows = n_rows
        self.n_columns = n_columns
        super().__init__(scene)
        self.grid = [[[] for _ in range(self.n_rows)] for _ in range(self.n_columns)]

    def clear(self):
        self.grid.clear()
        self.grid = [[[] for _ in range(self.n_rows)] for _ in range(self.n_columns)]


    def build(self):
        # Builds grid
        for circle in self.scene.circles:
            column_index, row_index = self._calculate_point_indices(circle.center)
            self.grid[column_index][row_index].append(circle)

    def _calculate_point_indices(self, point: Vector2) -> (int, int):
            """Given a point, returns the indices that can access to it's corresponding square in the grid"""
            # Calculates circle indices in grid
            colum_index = int((point.x - self.root_rectangle.left) / self.root_rectangle.width * self.n_columns)
            row_index = int((point.y - self.root_rectangle.bottom) / self.root_rectangle.height * self.n_rows)

            # Clamps to correct index interval
            colum_index = clamp(0, self.n_columns - 1, colum_index)
            row_index = clamp(0, self.n_rows - 1, row_index)
            return colum_index, row_index

    def get_overlapping(self, point: Vector2):
        """Returns all the circles that contain that point"""

        overlapping_circles = []
        column_index, row_index = self._calculate_point_indices(point)
        square_circles = self.grid[column_index][row_index]
        for circle in square_circles:

            if circle.overlaps_point(point):
                overlapping_circles.append(circle)

        return overlapping_circles
    

    def render(self, surface):

        # Renders all the squares
        cell_width = self.root_rectangle.width / self.n_columns
        cell_height = self.root_rectangle.height / self.n_rows
        left = self.root_rectangle.left
        bottom = self.root_rectangle.bottom

        SQUARE_OUTLINE_COLOR = (0, 0, 0)

        for column in range(self.n_columns):
            for row in range(self.n_rows):
                pg.draw.rect(
                    surface,
                    SQUARE_OUTLINE_COLOR,
                    (
                        left + cell_width * column,
                        bottom + cell_height * row, 
                        cell_width, 
                        cell_height
                    ),
                    2
                )
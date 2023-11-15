from pygame import Vector2

class Rectangle:

    def __init__(
            self, 
            min_edge : Vector2, 
            max_edge : Vector2
            ) -> None:
        self.min_edge = min_edge
        self.max_edge = max_edge
    
    @property
    def left(self):
        return self.min_edge.x
    
    @property
    def right(self):
        return self.max_edge.x
    
    @property
    def bottom(self):
        return self.min_edge.y
    
    @property
    def top(self):
        return self.max_edge.y
    
    @property
    def width(self):
        return self.max_edge.x - self.min_edge.x
    
    @property
    def height(self):
        return self.max_edge.y - self.min_edge.y

    def contains(self, point: Vector2) -> bool:
        """True if point is contained in rectangle"""
        return point.x >= self.left and point.x <= self.right and point.y >= self.bottom and point.y <= self.top
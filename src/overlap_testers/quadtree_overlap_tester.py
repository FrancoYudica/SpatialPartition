from ..overlap_tester import *
import pygame as pg


def clamp(min_value, max_value, clamp_value):
    if clamp_value < min_value:
        return min_value
    
    if clamp_value > max_value:
        return max_value
    
    return clamp_value


class QuadNode:

    def __init__(self, rectangle: Rectangle) -> None:
        self.rectangle = rectangle
        self.children = []
        self.is_empty = True
        self.is_leaf = True
        self.circle = None


    def add_circle(self, circle: Circle):

        if self.is_leaf:
            
            # When first circle is added
            if self.is_empty:
                self.circle = circle
                self.is_empty = False
                return

            # When node already has a circle, it 
            # splits, and adds the circle into children
            self.is_leaf = False
            self._split()
            self._add_in_children(self.circle)
            self.circle = None

        self._add_in_children(circle)

    
    def _split(self):
        # Builds children -------------------------------------------------------------------------------------
        child_size = 0.5 * Vector2(self.rectangle.width, self.rectangle.height)

        # Min points for each one of the new QuadNode
        min_bottom_left_rect = Vector2(self.rectangle.left, self.rectangle.bottom)
        min_top_left_rect = Vector2(self.rectangle.left, self.rectangle.top - child_size.y)
        min_bottom_right_rect = Vector2(self.rectangle.right - child_size.x, self.rectangle.bottom)
        min_top_right_rect = Vector2(self.rectangle.right - child_size.x, self.rectangle.top - child_size.y)

        self.children = [
            QuadNode(Rectangle(min_bottom_left_rect, min_bottom_left_rect + child_size)),
            QuadNode(Rectangle(min_top_left_rect, min_top_left_rect + child_size)),
            QuadNode(Rectangle(min_bottom_right_rect, min_bottom_right_rect + child_size)),
            QuadNode(Rectangle(min_top_right_rect, min_top_right_rect + child_size))
        ]

    def _add_in_children(self, circle: Circle):
        # Tests for overlap in children and adds
        # circle to corresponding child

        for child in self.children:
            # When node contains point
            overlaps_rect = child.rectangle.contains(circle.center)
            if overlaps_rect:
                child.add_circle(circle)
                return
            
    def get_overlapping(self, point: Vector2):

        # Node is empty, no overlaps
        if self.is_empty:
            return []

        # Node is a leaf, and contains exactly one circle, since it isn't empty
        if self.is_leaf:
            
            # Overlaps one circle
            if self.circle.overlaps_point(point):
                return [self.circle]
            
            # No overlaps
            return []
        
        # Node isn't a leaf, it's split onto 4 child QuadNode
        for child in self.children:
            
            # When node contains point
            overlaps_rect = child.rectangle.contains(point)
            if overlaps_rect:
                return child.get_overlapping(point)
            
        return []
        



class QuadTreeOverlapTester(OverlapTester):
    """
    Implements a QuadTree acceleration data structure.
    """
    def __init__(
            self,
            scene: CircleScene
            ) -> None:

        super().__init__(scene)
        self.root_node = QuadNode(self.root_rectangle)

    def clear(self):
        self.root_node = QuadNode(self.root_rectangle)
        
    def build(self):
        # Builds quad tree
        for circle in self.scene.circles:
            self.root_node.add_circle(circle)

    def get_overlapping(self, point: Vector2):
        return self.root_node.get_overlapping(point)

    def render(self, surface):
        SQUARE_OUTLINE_COLOR = (0, 0, 0)
        THICKNESS = 2
        # Breadth first search used to render tree
        quad_nodes = [self.root_node]

        while len(quad_nodes) > 0:
            quad_node = quad_nodes.pop(0)

            # Adds children for next iterations
            if not quad_node.is_leaf:
                quad_nodes.extend(quad_node.children)

            pg.draw.rect(
                surface,
                SQUARE_OUTLINE_COLOR,
                (
                    quad_node.rectangle.left,
                    quad_node.rectangle.bottom,
                    quad_node.rectangle.width + THICKNESS,
                    quad_node.rectangle.height + THICKNESS
                ),
                THICKNESS
            )

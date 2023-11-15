import pygame as pg
import random
from pygame import Vector2
from src.rectangle import Rectangle

from src.overlap_tester import OverlapTester, CircleScene
from src.overlap_testers.simple_overlap_tester import SimpleRegionOverlapTester
from src.overlap_testers.grid_overlap_tester import GridOverlapTester
from src.overlap_testers.quadtree_overlap_tester import QuadTreeOverlapTester
import json


def test_scene(overlap_tester: OverlapTester):
    pg.init()

    # Display size matches the root rectangle size
    DISPLAY_SIZE = overlap_tester.root_rectangle.width, overlap_tester.root_rectangle.height

    BACKGROUND_COLOR = (50, 50, 50, 255)
    CIRCLE_COLOR = (0, 255, 0, 255)
    CIRCLE_OVERLAP_COLOR = (255, 0, 0, 255)
    window = pg.display.set_mode(DISPLAY_SIZE)
    pg.display.set_caption("Spatial partition")
    running = True
    while running:

        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False
                break

            elif event.type == pg.MOUSEBUTTONDOWN:
                overlap_tester.scene.add_circle(Vector2(event.pos))
                overlap_tester.clear()
                overlap_tester.build()
        # Sets background color
        window.fill(BACKGROUND_COLOR)

        # Renders all circles
        for circle in overlap_tester.scene.circles:
            pg.draw.circle(
                surface=window,     
                color=CIRCLE_COLOR,
                center=circle.center,
                radius=circle.radius
            )

        # Gets mouse position, and tests if mouse is over any circle
        mouse = Vector2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
        overlapping_circles = overlap_tester.get_overlapping(mouse)

        # Renders all overlapping circles
        for circle in overlapping_circles:
            pg.draw.circle(
                surface=window,     
                color=CIRCLE_OVERLAP_COLOR,
                center=circle.center,
                radius=circle.radius
            )

        # Renders overlap tester visualization
        overlap_tester.render(window)

        pg.display.flip()


def generate_random_points(rectangle: Rectangle, count: int, seed: int):
    """Generates 'count' random points inside rectangle surface"""
    points = []

    # Sets seed, to get persistent results
    random.seed(seed)

    # Generates all the circles inside the provided rectangular surface
    for _ in range(count):
        position = Vector2(
            rectangle.left + rectangle.width * random.random(),
            rectangle.bottom + rectangle.height * random.random()
        )
        points.append(position)

    return points


def serialize_performance_test():
    area_size = 1000, 1000
    root_rectangle = Rectangle(Vector2(0, 0), Vector2(area_size))

    # Amount of randomly generated circles for each scene
    circles_count = 10000

    # Amount of randomly generated points for testing performance
    points_count = 100

    # Amount of samples
    n = 60

    grid_size = 10, 10


    data = {
        "AreaSize" : area_size,
        "CirclesCount" : circles_count,
        "RandomPointsCount" : points_count,
        "Samples" : n,
        "GridSize" : grid_size,
        "SamplesSimple" : [],
        "SamplesGrid" : [],
        "SamplesQuadTree" : []
    }


    for scene_index in range(n):
        print("Running scene:", scene_index)
        # Generates random scene
        scene = CircleScene(circles_count, scene_index, root_rectangle)

        # Creates all the testers
        simple_overlap_tester = SimpleRegionOverlapTester(scene)
        grid_overlap_tester = GridOverlapTester(grid_size[0], grid_size[1], scene)
        quad_tree_overlap_tester = QuadTreeOverlapTester(scene)

        # Builds all the acceleration data structures
        simple_overlap_tester.build()
        grid_overlap_tester.build()
        quad_tree_overlap_tester.build()

        # Generates the random test points
        random_points = generate_random_points(scene.root_rectangle, points_count, scene_index)

        # Measures time
        simple_sample_time = simple_overlap_tester.measure_overlapping_time(random_points)
        grid_sample_time = grid_overlap_tester.measure_overlapping_time(random_points)
        quad_tree_sample_time = quad_tree_overlap_tester.measure_overlapping_time(random_points)

        # Stores results
        data["SamplesSimple"].append(simple_sample_time)
        data["SamplesGrid"].append(grid_sample_time)
        data["SamplesQuadTree"].append(quad_tree_sample_time)

    # Serializes data to json file
    with open("samples.json", 'w') as file:
        json.dump(data, file, indent='\t')

    print("End of serialization")

if __name__ == "__main__":
    area_size = 500, 500
    root_rectangle = Rectangle(Vector2(0, 0), Vector2(area_size))
    scene = CircleScene(0, 0, root_rectangle)
    # overlap_tester = SimpleRegionOverlapTester(scene)
    # overlap_tester = GridOverlapTester(5, 5, scene)
    overlap_tester = QuadTreeOverlapTester(scene)
    overlap_tester.build()
    test_scene(overlap_tester)

    # serialize_performance_test()
    


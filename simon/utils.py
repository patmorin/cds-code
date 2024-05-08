import argparse
import collections
import math
import random
import sys
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt
import scipy
import scipy.spatial

import message

COLLINEAR: str = "collinear"
RANDOM_DISK: str = "random points in disk"
RAND_TRI: str = "random points in triangle"
RED = "\033[0;31m"
EDGE_COUNT = 3


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=message.DESCRIPTION)

    parser.add_argument(
        "N",
        type=positive_int,
        nargs="?",
        default=10,
        help="the number of points to use (default: 10)",
    )

    parser.add_argument(
        "-c", "--collinear", action="store_true", help=message.COLLINEAR_ARG
    )
    parser.add_argument(
        "-d", "--randisk", action="store_true", default=True, help=message.RP_DISK_ARG
    )
    parser.add_argument(
        "-t", "--rantri", action="store_true", help=message.RP_TRIANGLE_ARG
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    return args


def positive_int(value: Any) -> int:
    int_value = int(value)

    if int_value <= 0:
        raise argparse.ArgumentTypeError(
            f"{value} is an invalid number of points to be used. N > 0"
        )

    return int_value


def collect_args(args: argparse.Namespace) -> Tuple[int, str]:
    point_count: int = args.N

    if args.collinear:
        data_type: str = COLLINEAR
    elif args.rantri:
        data_type: str = RAND_TRI
    else:
        data_type: str = RANDOM_DISK

    return point_count, data_type


def create_graph(
    point_count: int, data_type: str
) -> Tuple[List[Tuple[float, float]], List[List[int]]]:
    print(f"Step 1: Generating {data_type} point set of size {point_count}...")
    points: List[Tuple[float, float]] = generate_points(point_count, data_type)

    print(message.STEP_2)
    faces: List = delaunay_triangulation(points)

    return points, faces


def generate_points(point_count: int, data_type: str) -> List[Tuple[float, float]]:
    if data_type == RANDOM_DISK:  # use a set of n - 3 random points
        points = [(-1.5, -1.5), (-1.5, 3), (3, -1.5)] + [
            gen_unit_circ_point() for _ in range(point_count - 3)
        ]
    elif data_type == COLLINEAR:  # use a set of n - 3 collinear points
        points = [(-1.5, -1.5), (-1.5, 3), (3, -1.5)] + [
            (-1 + i / (point_count - 3), -1 + i / (point_count - 3))
            for i in range(point_count - 3)
        ]
    elif data_type == RAND_TRI:
        points = [(0, 0), (1, 1), (1, 0)] + [
            (random.random(), random.random()) for _ in range(point_count - 3)
        ]
        for i in range(point_count):
            (x, y) = points[i]
            if x < y:
                points[i] = (y, x)

    return points


def gen_unit_circ_point() -> Tuple[float, float]:
    while 1 < 2:
        x = 2 * random.random() - 1
        y = 2 * random.random() - 1
        if math.pow(x, 2) + math.pow(y, 2) < 1:
            return (x, y)


def delaunay_triangulation(points: List[Tuple[float, float]]) -> List[List[int]]:
    delaunay_triangulation: Any = scipy.spatial.Delaunay(points)
    faces: List[List[int]] = list()

    for face in delaunay_triangulation.simplices:
        faces.append(list(face))

    return faces


def map_edge(faces: List[List[int]]) -> Dict[Tuple[int, int], int]:
    print(message.STEP_3)

    faces_map = dict()
    outer_face_edges = set()

    for face_id, face in enumerate(faces):
        for i in range(EDGE_COUNT):
            cc_edge: Tuple[int, int] = (
                face[i],
                face[(i + 1) % EDGE_COUNT],
            )  # a edge in the counter-clockwise direction
            faces_map[cc_edge] = collections.deque([face_id])

            reversed_cc_edge: Tuple[int, int] = cc_edge[::-1]
            if reversed_cc_edge in faces_map:
                outer_face_edges.remove(reversed_cc_edge)
            else:
                outer_face_edges.add(cc_edge)

    return outer_face_edges


def draw_graph(points: List[Tuple[float, float]], faces: List[List[int]]) -> None:
    print(message.STEP_4)
    sys.stdout.write(RED)
    print(message.STEP_4_WARNING)

    for face in faces:
        for i in range(3):
            plt.plot(
                [points[face[i]][0], points[face[(i + 1) % 3]][0]],
                [points[face[i]][1], points[face[(i + 1) % 3]][1]],
                color="black",
            )

    for point in points:
        plt.plot(
            point[0],
            point[1],
            color="red",
            lw=1,
            marker="o",
            markersize=min(8, 180 / len(points)),
        )

    plt.show()

import argparse
import random
import sys
from typing import Any, Dict, List, Set, Tuple

import matplotlib.pyplot as plt
import scipy
import scipy.spatial  # linux

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
    points = generate_initial_points(data_type)
    additional_count = point_count - len(points)

    if data_type == RANDOM_DISK:
        points += [gen_unit_circ_point() for _ in range(additional_count)]
    elif data_type == COLLINEAR:
        points += [(-1 + i / additional_count, -1 + i / additional_count) for i in range(additional_count)]
    elif data_type == RAND_TRI:
        additional_points = [(random.random(), random.random()) for _ in range(additional_count)]
        points += [(max(x, y), min(x, y)) for x, y in additional_points]  # ensure x < y for each point, swapping if necessary

    return points


def generate_initial_points(data_type: str) -> List[Tuple[float, float]]:
    if data_type == RANDOM_DISK or data_type == COLLINEAR:
        return [(-1.5, -1.5), (-1.5, 3), (3, -1.5)]
    elif data_type == RAND_TRI:
        return [(0, 0), (1, 1), (1, 0)]


def gen_unit_circ_point() -> Tuple[float, float]:
    while True:
        x = 2 * random.random() - 1
        y = 2 * random.random() - 1
        if x**2 + y**2 < 1:
            return (x, y)


def delaunay_triangulation(points: List[Tuple[float, float]]) -> List[List[int]]:
    delaunay_triangulation: Any = scipy.spatial.Delaunay(points)
    faces: List[List[int]] = list()

    for face in delaunay_triangulation.simplices:
        faces.append(list(face))

    return faces


def classify_edge(faces: List[List[int]]) -> Dict[Tuple[int, int], int]:
    print(message.STEP_3)

    edge_face_map: Dict[Tuple[int, int], int] = dict()
    outer_face_edges: Set[Tuple[int, int]] = set()

    for face_id, face in enumerate(faces):
        for i in range(EDGE_COUNT):
            cc_edge: Tuple[int, int] = (
                face[i],
                face[(i + 1) % EDGE_COUNT],
            )  # a edge in the counter-clockwise direction
            edge_face_map[cc_edge] = face_id

            track_outer_face(cc_edge, outer_face_edges)

    add_outer_face(
        len(faces), outer_face_edges, edge_face_map
    )  # allocate a face id for the outerface. it's len(faces) since dynamic arrays start from 0 to n - 1, so by selecting len(faces), we're effectively doing n - 1 + 1 = n

    return edge_face_map


def track_outer_face(
    cc_edge: Tuple[int, int], outer_face_edges: Set[Tuple[int, int]]
) -> None:
    reversed_cc_edge: Tuple[int, int] = cc_edge[::-1]
    if reversed_cc_edge in outer_face_edges:
        outer_face_edges.remove(reversed_cc_edge)
    else:
        outer_face_edges.add(cc_edge)


def add_outer_face(
    outer_face_id: int,
    outer_face_edges: Set[Tuple[int, int]],
    edge_face_map: Dict[Tuple[int, int], int],
) -> None:
    for c_edge in outer_face_edges:
        cc_edge: Tuple[int, int] = c_edge[
            ::-1
        ]  # make the actual edge of each face counter-clockwise
        edge_face_map[cc_edge] = outer_face_id


def draw_graph(points: List[Tuple[float, float]], faces: List[List[int]]) -> None:
    print(message.STEP_5)
    sys.stdout.write(RED)
    print(message.STEP_5_WARNING)

    plot_black_edges(points, faces)

    plot_points(points)

    plt.show()


def plot_black_edges(points, faces) -> None:
    for face in faces:
        for i in range(EDGE_COUNT):
            start_point = points[face[i]]
            end_point = points[face[(i + 1) % EDGE_COUNT]]
            plt.plot(
                [start_point[0], end_point[0]],
                [start_point[1], end_point[1]], 
                color="black",
            )

def plot_points(points) -> None:
    for point in points:
        plt.plot(
            point[0],
            point[1],
            color = "red",
            lw = 1,
            marker = "o",
            markersize = min(8, 180 / len(points)),
        )



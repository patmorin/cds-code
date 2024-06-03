import argparse
import collections
import random
import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.spatial  # linux

import message

COLLINEAR: str = "collinear"
RANDOM_DISK: str = "random points in disk"
RAND_TRI: str = "random points in triangle"
EDGE_COUNT = 3


def parse_args():
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


def positive_int(value):
    int_value = int(value)

    if int_value <= 0:
        raise argparse.ArgumentTypeError(
            f"{value} is an invalid number of points to be used. N > 0"
        )

    return int_value


def collect_args(args):
    point_count = args.N

    if args.collinear:
        data_type = COLLINEAR
    elif args.rantri:
        data_type = RAND_TRI
    else:
        data_type = RANDOM_DISK

    return point_count, data_type


def generate_points(point_count, data_type):
    points = gen_initial_points(data_type)
    additional_count = point_count - len(points)

    if data_type == RANDOM_DISK:
        points += [gen_unit_circ_point() for _ in range(additional_count)]
    elif data_type == COLLINEAR:
        points += [
            (-1 + i / additional_count, -1 + i / additional_count)
            for i in range(additional_count)
        ]
    elif data_type == RAND_TRI:
        additional_points = [
            (random.random(), random.random()) for _ in range(additional_count)
        ]
        points += [
            (max(x, y), min(x, y)) for x, y in additional_points
        ]  # ensure x < y for each point, swapping if necessary

    return points


def gen_initial_points(data_type):
    if data_type == RANDOM_DISK or data_type == COLLINEAR:
        return [(-1.5, -1.5), (-1.5, 3), (3, -1.5)]
    elif data_type == RAND_TRI:
        return [(0, 0), (1, 1), (1, 0)]


def gen_unit_circ_point():
    while True:
        x = 2 * random.random() - 1
        y = 2 * random.random() - 1
        if x**2 + y**2 < 1:
            return (x, y)


def compute_delaunay_triangulation(points):
    points_array = np.array(points)
    delaunay_triangulation = scipy.spatial.Delaunay(points_array)
    return delaunay_triangulation.simplices


def collect_faces(delaunay_triangulation):
    faces = list()

    for face in delaunay_triangulation:
        faces.append(list(face))

    return faces


def classify_edge(faces):
    edge_face_map = dict()
    outer_face_edges = set()

    for face_id, face in enumerate(faces):
        for i in range(EDGE_COUNT):
            cc_edge = (
                face[i],
                face[(i + 1) % EDGE_COUNT],
            )  # a edge in the counter-clockwise direction
            edge_face_map[cc_edge] = face_id

            track_outer_face(cc_edge, outer_face_edges)

    add_outer_face(
        len(faces), outer_face_edges, edge_face_map
    )  # allocate a face id for the outerface. it's len(faces) since dynamic arrays start from 0 to n - 1, so by selecting len(faces), we're effectively doing n - 1 + 1 = n

    return edge_face_map


def track_outer_face(cc_edge, outer_face_edges):
    reversed_cc_edge = cc_edge[::-1]
    if reversed_cc_edge in outer_face_edges:
        outer_face_edges.remove(reversed_cc_edge)
    else:
        outer_face_edges.add(cc_edge)


def add_outer_face(
    outer_face_id,
    outer_face_edges,
    edge_face_map,
):
    for c_edge in outer_face_edges:
        cc_edge = c_edge[::-1]  # make the actual edge of each face counter-clockwise
        edge_face_map[cc_edge] = outer_face_id


def create_adjacency_list(faces):
    adjacency_list = collections.defaultdict(set)

    for face in faces:
        for vertex in face:
            complement = list(set(face) - {vertex})
            adjacency_list[vertex].add(complement[0])
            adjacency_list[vertex].add(complement[1])

    return adjacency_list


def draw_graph(points, delaunay_triangulation):
    points_array = np.array(points)

    print(points_array)

    plt.triplot(
        points_array[:, 0], points_array[:, 1], delaunay_triangulation, color="black"
    )

    plt.plot(points_array[:, 0], points_array[:, 1], "o", markersize = 15)

    print(delaunay_triangulation)

    # point labelling
    for integer_label, point in enumerate(points):
        plt.text(point[0], point[1], integer_label, ha = "center", va = "center", fontsize = 10, color='white') 

    # face labelling
    for integer_label, face_index in enumerate(delaunay_triangulation):
        point = points_array[face_index].mean(axis = 0)
        plt.text(point[0], point[1], integer_label, ha = "center", va = "center", fontsize = 10)

    plt.show()
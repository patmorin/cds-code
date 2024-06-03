#!/usr/bin/env python3

import message
import utils


def main():
    args = utils.parse_args()

    point_count, data_type = utils.collect_args(args)

    print(f"Step 1: Generating {data_type} point set of size {point_count}...")
    points = utils.generate_points(point_count, data_type)

    print(message.STEP_2)
    delaunay_triangulation = utils.compute_delaunay_triangulation(points)

    print(message.STEP_3)
    faces = utils.collect_faces(delaunay_triangulation)
    edge_face_map = utils.classify_edge(faces)
    
    print(message.STEP_4)
    adjacency_list = utils.create_adjacency_list(faces)

    print(message.STEP_5)
    print(message.STEP_5_WARNING)
    utils.draw_graph(points, delaunay_triangulation)


if __name__ == "__main__":
    main()

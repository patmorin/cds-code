#!/usr/bin/env python3

import argparse
from typing import Tuple

import utils


def main() -> None:
    args: argparse.Namespace = utils.parse_args()

    point_count, data_type = utils.collect_args(args)  # Tuple[int, str]

    points, faces = utils.create_graph(
        point_count, data_type
    )  # Tuple[List[Tuple[float, float]], List[List[int]]]

    edge_face_map: Tuple[int, int] = utils.classify_edge(faces)

    # TODO: adjacency list

    # TODO: mpl avg x avg y face label

    # TODO: mpl link between faces

    utils.draw_graph(points, faces)


if __name__ == "__main__":
    main()

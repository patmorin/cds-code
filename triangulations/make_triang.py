#!/usr/bin/python3
import sys
import time
import random
import itertools
import matplotlib.pyplot as plt
import scipy.spatial


def triangulate(points):
    n = len(points)
    dt = scipy.spatial.Delaunay(points)
    assert(dt.npoints == n)
    assert(len(dt.convex_hull) == 3)
    assert(dt.nsimplex == 2*n - 5)
    return [list(t) for t in dt.simplices]



######################################################################
# Boring routines to build a "random" triangulation
######################################################################
def make_triangulation(n, data_type):
    print("Generating points")
    if data_type == 0:
        # Use a set of n-3 random points
        points = [(-1.5,-1.5), (-1.5,3), (3,-1.5)] \
                 + [random_point() for _ in range(n-3)]
    elif data_type == 1:
        # Use a set of n-3 collinear points
        points = [(-1.5,-1.5), (-1.5,3), (3,-1.5)] \
                 + [(-1 + i/(n-3), -1 + i/(n-3)) for i in range(n-3)]
    elif data_type == 2:
        points = [(0, 0), (1,1), (1,0)] \
                 + [(random.random(), random.random()) for _ in range(n-3)]
        for i in range(n):
            (x, y) = points[i]
            if x < y:
                points[i] = (y, x)
    else:
        raise ValueError("Invalid argument for data_type")

    n = len(points)
    # random.shuffle(points)

    print("Computing Delaunay triangulation")
    triangles = triangulate(points)
    return list(points), triangles

""" Generate a random point in the unit circle """
def random_point():
    while 1 < 2:
        x = 2*random.random()-1
        y = 2*random.random()-1
        if x**2 + y**2 < 1:
            return (x, y)


def usage():
    print("Make a Delaunay triangulation")
    print("Usage: {} [-h] [-c] [-r] [-y] [-w] [-b] <n>".format(sys.argv[0]))
    print("  -h show this message")
    print("  -c use collinear points")
    print("  -y use random points in triangle")
    print("  -r use random points in disk (default)")
    print("  <n> the number of points to use (default = 10)")

if __name__ == "__main__":
    n = 0
    data_type = 0
    worst_case = True
    verify = True
    for arg in sys.argv[1:]:
        if arg == '-h':
            usage()
        elif arg == '-r':
            data_type = 0   # random
        elif arg == '-c':
            data_type = 1   # collinear
        elif arg == '-y':
            data_type = 2   # random in triangle (like rbox y)
        else:
            n = int(arg)

    if n <= 0:
        usage()
        sys.exit(-1)

    s = ["random", "collinear", "uniform"][data_type]
    print("Generating {} point set of size {}".format(s, n))
    points, triangles = make_triangulation(n, data_type)

    print("Warning: There is no triangle representing the outer face")

    print(points)
    print(triangles)
    # Draw graph
    for t in triangles:
        print(t)
        for i in range(3):
            plt.plot([points[t[i]][0], points[t[(i+1)%3]][0]], [points[t[i]][1], points[t[(i+1)%3]][1]], color='black')

    for p in points:
        plt.plot(p[0], p[1], color="red", lw=1, marker='o',
                 markersize=min(8,180/n))



    # Draw tripods

    plt.axis('off')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

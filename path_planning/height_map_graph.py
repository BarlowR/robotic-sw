import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.cm as cm

from PIL import Image, ImageOps
import sys

import utils.map_preprocessing as mpp
import utils.graph as graph
import rrt.rrt as rrt


def plot_edges(graph, img, i):
    for start, ends in graph.edges.items():
        for (end, cost) in ends:

            x = (start[1], end[1])
            y = (start[0], end[0])

            path, cost = graph.find_path_cost((10,420), end)

            img.plot(x, y, color = cm.twilight((cost%1000)/1000))


if __name__ == "__main__":


    start = (10,420)
    end = (80,20)

    environment_map = mpp.load("rrt/hm.jpg")
    plt.imshow(environment_map, cmap = 'gray')

    pathplanning_graph = graph.DirectedGraph(2)
    pathplanning_graph.load("pathmap.pkl")

    print("drawing...")
    plt.cla()
    plt.imshow(environment_map, cmap = 'gray')
    plot_edges(pathplanning_graph, plt, 1)

    plt.show()




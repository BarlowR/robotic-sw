import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.cm as cm

from PIL import Image, ImageOps
import sys

import utils.map_preprocessing as mpp
import utils.graph as graph
import rrt.rrt as rrt


def plot_lines(graph, ax, environment):
    for start, ends in graph.edges.items():
        for (end, cost) in ends:

            x = (start[1], end[1])
            y = (start[0], end[0])
            z = (environment[start]+5, environment[end]+5)

            #path, cost = graph.find_path_cost((10,420), end)

            cost = 700
            ax.plot(x, y, z, color = (0.8, 0.2, 0.5), linewidth = 1.5)


if __name__ == "__main__":


    environment_map = mpp.load("rrt/hm.jpg")

    pathplanning_graph = graph.DirectedGraph(2)
    pathplanning_graph.load("pathmap.pkl")

    x, y = np.meshgrid(range(environment_map.shape[1]), range(environment_map.shape[0]))

    print(x.shape, y.shape, environment_map.shape)


    fig = plt.figure(frameon = False)
    fig.tight_layout()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(x, y, environment_map, color = "green", alpha = 0.5)
    #ax.contour(x,y,environment_map, cmap = "gray", levels = 40)
    ax.set_aspect("auto")
    ax.set_box_aspect((10,5,1))
    ax.axis("off")

    plot_lines(pathplanning_graph, ax, environment_map)

    #ax.set_xlim(mean_x - max_range, mean_x + max_range)
    #ax.set_ylim(mean_y - max_range, mean_y + max_range)
    plt.show()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.cm as cm

from PIL import Image, ImageOps
import sys

import utils.environment_map as map_utils
import utils.graph as graph
import rrt.rrt as rrt


def plot_edges(nodes, img):
    for start, node in nodes.items():
        for child in node.children:

            x = (start[1], child[1])
            y = (start[0], child[0])
            img.plot(x, y, color = cm.twilight((node.cost%1000)/1000))



if __name__ == "__main__":


    start = (200,50)
    end = (80,20)

    environment_map = map_utils.load_heightmap("rrt/hm2.jpg")
    plt.imshow(environment_map, cmap = 'gray')

    pathplanning_graph = graph.NodeTree(start)
    #pathplanning_graph.load("pathmap.pkl")


    for i in range(1000):
        print("iteration {}".format(i))
        rrt.RRT_star(environment_map, pathplanning_graph, start, end, 4, 1000, 7, rrt.elevation_change_cost, lambda x,y,z: rrt.elevation_change_passable(x, y, 1, .2, z))
        pathplanning_graph.save("pathmap.pkl")
        plt.cla()
        plt.imshow(environment_map, cmap = 'gray')
        plot_edges(pathplanning_graph.nodes, plt)
        plt.pause(.1)

    plt.show()




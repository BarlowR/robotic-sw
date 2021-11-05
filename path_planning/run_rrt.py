import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
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
            img.plot(x, y, color = (1, node.cost/1000, 0))


if __name__ == "__main__":


    start = (50,50)
    end = (80,20)

    fig = plt.figure(1, (4., 4.))
    grid = ImageGrid(fig, 111,  # similar to subplot(111)
                 nrows_ncols=(2, 2),  # creates 2x2 grid of axes
                 axes_pad=0.1,  # pad between axes in inch.
                 )

    environment_map = map_utils.load_heightmap("rrt/hm.jpg")
    grid[0].imshow(environment_map, cmap = 'gray')

    pathplanning_graph = graph.NodeTree((0,0))

    for i in range(1,4):
        rrt.RRT(environment_map, pathplanning_graph, start, end, 5, 500, lambda x,y,z: 3, lambda x,y,z: True)
        grid[i].imshow(environment_map, cmap = 'gray')
        plot_edges(pathplanning_graph.nodes, grid[i])


   

    plt.show()




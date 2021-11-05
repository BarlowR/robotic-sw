import numpy as np

import path_planning.utils.environment_map as map_utils
import path_planning.utils.graph as graph
import path_planning.rrt.rrt as rrt

test_vertex_1 = (1,1,1)

test_vertex_2 = (4,6,1)

test_vertex_3 = (2,2,1)

test_vertex_4 = (3,15,9)

test_vertex_5 = (4,4,4)

test_vertex_6 = (7,7,7)

test_vertex_7 = (9,9,9)

def test_map_load():
    print("testing load method")
    test_load = map_utils.load_heightmap("tests/test_map.png")
    assert test_load.ndim == 2, "incorrect dimensions"
    assert test_load.max() < 256 and test_load.min() >= 0, "value out of bounds"
    assert type(test_load[0,0]) == np.uint8, "incorrect datatype"


def test_DirectedGraph():

    test_graph = graph.DirectedGraph(3)

    #add_vertex
    assert test_graph.add_vertex(test_vertex_1)
    assert test_graph.add_vertex(test_vertex_2)
    assert test_graph.add_vertex(test_vertex_3)
    assert not test_graph.add_vertex(test_vertex_2)

    #remove_vertex
    assert test_graph.remove_vertex(test_vertex_2)
    assert not test_graph.remove_vertex(test_vertex_4)

    #is_vertex
    assert test_graph.is_vertex(test_vertex_1)
    assert not test_graph.is_vertex(test_vertex_2)
    assert test_graph.add_vertex(test_vertex_2)


    #add_edge
    assert test_graph.add_edge(test_vertex_1, test_vertex_2, 4)
    assert test_graph.add_edge(test_vertex_2, test_vertex_1, 4)
    assert test_graph.add_edge(test_vertex_2, test_vertex_3, 6)
    assert not test_graph.add_edge(test_vertex_1, test_vertex_4, 5)

    #remove_edge
    assert test_graph.add_vertex(test_vertex_4)
    assert test_graph.add_edge(test_vertex_1, test_vertex_4, 4)
    assert test_graph.remove_edge(test_vertex_1, test_vertex_4)

    #is_edge
    assert test_graph.is_edge(test_vertex_1, test_vertex_2)
    assert not test_graph.is_edge(test_vertex_1, test_vertex_4)


    assert test_graph.find_path_cost(test_vertex_1, test_vertex_3) \
            == ([test_vertex_1, test_vertex_2, test_vertex_3], 10) 

    assert test_graph.save("graph.pkl")

    assert test_graph.remove_edge(test_vertex_1, test_vertex_2)
    assert test_graph.load("graph.pkl")
    assert test_graph.is_edge(test_vertex_1, test_vertex_2)


def test_NodeTree():

    start_node = (0,0,0)

    test_graph = graph.NodeTree(start_node)

    #add_node
    assert test_graph.add_node(test_vertex_1, start_node, 5)
    assert test_graph.add_node(test_vertex_2, start_node, 5)
    assert test_graph.add_node(test_vertex_3, test_vertex_1, 5)
    assert not test_graph.add_node((1,2,3), test_vertex_4, 5)       #shouldn't be able to add with non-existent parent


    #remove_node
    assert test_graph.add_node(test_vertex_5, start_node, 5)
    assert test_graph.add_node(test_vertex_6, test_vertex_5, 6)
    assert test_graph.add_node(test_vertex_7, test_vertex_5, 7)

    assert test_graph.remove_node(test_vertex_5)
    assert (not test_vertex_7 in test_graph.nodes                   
            and not test_vertex_6 in test_graph.nodes
            and not test_vertex_5 in test_graph.nodes)              # all child nodes should be removed

    assert not test_graph.remove_node(test_vertex_6)              # shouldn't be able to remove a node that isn't there

    #change_parent
    assert test_graph.add_node(test_vertex_5, start_node, 5)
    assert test_graph.change_parent(test_vertex_5, test_vertex_2, 2)
    assert test_graph.nodes[test_vertex_5].parent == test_vertex_2

    #path_between_nodes
    assert test_graph.path_between_nodes(start_node, test_vertex_5) == \
            [start_node, test_vertex_2, test_vertex_5]

    assert not test_graph.path_between_nodes(start_node, test_vertex_7)


'''
def test_rrt():

    #setup
    test_graph = graph.DirectedGraph(3)
    test_map = map_utils.load_heightmap("tests/test_map.png")
    bounds = test_map.shape

    test_graph.add_vertex(test_vertex_1)
    test_graph.add_vertex(test_vertex_2)
    test_graph.add_vertex(test_vertex_3)

    #nearest_vertex
    assert rrt.nearest_node((2,2,2), test_graph.vertices) == test_vertex_3

    #new_vertex
    assert rrt.new_vertex(test_vertex_1, test_vertex_2, 3) == (3,4,1)
    #   min of q_rand and delta_q
    assert rrt.new_vertex(test_vertex_1, (2,1,1), 10 == (2,1,1))

    #near
    assert rrt.near((1,1,2), test_graph.vertices, 4) == \
            [test_vertex_1, test_vertex_3]
'''


if __name__ == "__main__":
    test_DirectedGraph()
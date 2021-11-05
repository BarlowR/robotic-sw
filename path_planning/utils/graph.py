import numpy as np
import pickle

class DirectedGraph:
    def __init__(self, d):
        #initialize an instance with given dimensions
        self.dimensions = d
        self.vertices = []
        self.edges = {}
        # dict of form { start_edge_1 : [(end_edge_1, cost) , (end_edge_2, cost)] }

    def is_vertex(self, vertex):
        # checks if a coordinate pair is a vertex in the graph
        if (len(self.vertices) == 0):
            return False
        
        return (vertex in self.vertices)

    def add_vertex(self, vertex):
        # add a vertex to the graph
        if len(vertex) == self.dimensions:

            if (len(self.vertices) == 0):
                self.vertices = [vertex]
                return True

            elif (not self.is_vertex(vertex)):
                self.vertices = self.vertices + [vertex]
                return True

        return False

    def remove_vertex(self, vertex):
        if (self.is_vertex(vertex)):
            self.vertices.remove(vertex)
            return True
        return False


    def add_edge(self, start_vertex, end_vertex, cost):
        # add an edge to the graph
        if (self.is_vertex(start_vertex) and self.is_vertex(end_vertex)):
            if start_vertex in self.edges:
                self.edges[start_vertex] = self.edges[start_vertex] + [(end_vertex, cost)]
            else:
                self.edges[start_vertex] = [(end_vertex, cost)]
            return True
        else:
            return False

    def remove_edge(self, start_vertex, end_vertex):
        if (self.is_edge(start_vertex, end_vertex)):
            if (len(self.edges[start_vertex]) > 1) :
                ends = self.edges[start_vertex] 
                for (end, cost) in ends:
                    if (end == end_vertex):
                        ends.remove((end, cost))
                        self.edges[start_vertex] = ends
                        return True
            else:
                del self.edges[start_vertex]
                return True
        return False

    def is_edge(self, start_vertex, end_vertex):
        # checks if a pair of vertices is a edge in the graph.
        if (start_vertex in self.edges):
            for (end, cost) in self.edges[start_vertex]:
                if (end == end_vertex):
                    return True
        return False

    def cost_edge(self, start_vertex, end_vertex):
        if (self.is_edge(start_vertex, end_vertex)):
            (end, cost) = self.edges[start_vertex]
            return cost
        return False

    def find_path_cost(self, start_vertex, end_vertex, path = None, total_cost = 0):
        # find a path from start_vertex to end_vertex in graph and record cost

        if path == None:
            path = []

        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return (path, total_cost)

        if start_vertex not in self.edges:
            return False

        for (vertex, cost) in self.edges[start_vertex]:
            if vertex not in path:
                if extended_path := self.find_path_cost(vertex, end_vertex, path, cost + total_cost):
                    return extended_path
        return False

    def save(self, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump((self.dimensions, self.vertices, self.edges), file)
            return True

    def load(self, filepath):
        with open(filepath, 'rb') as file:
            (self.dimensions, self.vertices, self.edges) = pickle.load(file)
            return True








class NodeTree:

    def __init__(self, first_node_vertex):
        first_node = rrtNode(first_node_vertex, 0, None, None)

        #self.dimensions = d                                     # dimensions of the environment  ***not sure if this is necessary?***
        self.nodes = {first_node_vertex : first_node}             # dictionary of form { node vertex : node }
        

    def add_node(self, vertex, parent, cost_to_parent):
        if parent in self.nodes:

            #pull the parent node from the dict
            parent_node = self.nodes[parent]
            cost_to_node = parent_node.cost + cost_to_parent

            #make a new node and add it to the dict of nodes
            new_node = rrtNode(vertex, cost_to_node, parent, cost_to_parent)
            self.nodes[vertex] = new_node
            
            #add the new node as a child of the parent node
            self.nodes[parent].children += [vertex]

            return True

        return False


    def remove_child(self, vertex, child):
        if vertex in self.nodes:
            if child in self.nodes[vertex].children:
                self.nodes[vertex].children.remove(child)
                return True

        return False


    def change_parent(self, vertex, new_parent, cost_to_new_parent):
        if (    vertex in self.nodes
            and new_parent in self.nodes):

            # remove child from old parent
            old_parent = self.nodes[vertex].parent
            self.remove_child(old_parent, vertex)

            # add child to new parent
            self.nodes[new_parent].children += [vertex]

            # change node values
            new_parent_cost = self.nodes[new_parent].cost
            self.nodes[vertex].parent = new_parent
            self.nodes[vertex].cost = new_parent_cost + cost_to_new_parent
            self.nodes[vertex].cost_to_parent = cost_to_new_parent

            return True

        return False


    def remove_node(self, vertex):
        # removes node and recursively removes all children of node

        if vertex in self.nodes:
            if self.nodes[vertex].children:
                for child in self.nodes[vertex].children:
                    if not self.remove_node(child):
                        return False
            del self.nodes[vertex]
            return True

        return False

    def path_between_nodes(self, parent, grandchild, path = []):
        
        path += [parent]
        
        if parent == grandchild:
            return path 

        elif self.nodes[parent].children:

            for child in self.nodes[parent].children:
                extended_path = self.path_between_nodes(child, grandchild, path.copy())  #path.copy() necessary to stop python from changing path inplace
                if extended_path:
                    return extended_path
        return False


    

    def save(self, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump(self.nodes, file)
            return True

        return False

    def load(self, filepath):
        with open(filepath, 'rb') as file:
            self.nodes = pickle.load(file)
            return True
        return False


class rrtNode:
    def __init__(self, vertex, cost, parent, cost_to_parent):
        #initialize a node
        self.vertex = vertex                    # n dimensional tuple with vector coordinates of node
        self.cost = cost                        # total cost to this node
        self.parent = parent                    # parent vertex
        self.cost_to_parent = cost_to_parent    # cost to parent
        self.children = []                # list of children
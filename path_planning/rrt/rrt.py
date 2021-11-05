import numpy as np 


def nearest_node(sample, nodes):
    #calculate the closest vertex to a given sample based on a distance method
    
    vertices = list(nodes.keys())
    best_node = vertices[0]
    least_dist = euclidean_distance(sample, best_node)
    for node in vertices:
        dist = euclidean_distance(sample, node)
        if dist < least_dist:
            best_node = node
            least_dist = dist 

    return best_node

def new_node(q_nearest, q_rand, delta_q):

    q_new = q_rand

    if euclidean_distance(q_nearest, q_rand) > delta_q:
        scaling_factor = delta_q / euclidean_distance(q_nearest, q_rand)
        delta = scaling_factor * (np.asarray(q_rand) - np.asarray(q_nearest))

        q_new = tuple(np.rint(delta + np.asarray(q_nearest)).astype(int))
        
    return q_new

def near(sample, nodes, threshold):
    nearby = []
    for node in nodes.keys():
        if euclidean_distance(sample, node) < threshold:              #potentially expensive call
            nearby.append(node)
    return nearby



def euclidean_distance(p, q):
    return np.linalg.norm(np.asarray(p) - np.asarray(q))





def RRT(environment, nodeTree, start, end, delta_q, iterations, cost, passable, found_path = False):
    # iteratively run RRT for given number of iterations to attempt to find a path to end. 

    print("")
    while (iterations):

        q_rand = tuple(np.random.randint(0, environment.shape))
        q_nearest = nearest_node(q_rand, nodeTree.nodes) #euclidean distance here used as placeholder
        q_new = new_node(q_nearest, q_rand, delta_q)

        if (passable(q_nearest, q_new, environment)):     
            nodeTree.add_node(q_new, q_nearest, cost(q_nearest, q_new, environment))

        if (euclidean_distance(q_new, end) < delta_q and passable(q_new, end, environment)):
            nodeTree.add_node(end, q_new, cost(q_new, end, environment))
            found_path = True

        if (iterations > 0):
            iterations = iterations - 1
        elif (found_path):
            break

        print("     ", end = '\r')
        print(iterations, end ='\r')
    return True



def RRT_star(environment, nodeTree, start, end, delta_q, iterations, threshold, cost, passable, found_path = False):
    # iteratively run RRT for given number of iterations to attempt to find a path to end. 

    while (iterations):

        q_rand = tuple(np.random.randint(0, environment.shape))
        q_nearest = nearest_node(q_rand, nodeTree.nodes) #euclidean distance here used as placeholder
        q_new = new_node(q_nearest, q_rand, delta_q)

        if (passable(q_nearest, q_new, environment)):  

            Q_near = near(q_new, nodeTree.nodes, threshold)

            q_min = q_nearest
            q_min_cost = nodeTree.nodes[q_nearest].cost
            q_min_cost += cost(q_nearest, q_new, environment)

            for q_near in Q_near:   #connect to min path cost vertex
                
                if passable(q_near, q_new, environment):
                    
                    q_near_cost = nodeTree.nodes[q_near].cost
                    q_near_cost += cost(q_near, q_new, environment)

                    if q_near_cost < q_min_cost:
                        q_min = q_near
                        q_min_cost = q_near_cost

            nodeTree.add_node(q_new, q_min, cost(q_min, q_new, environment))



            for q_near in Q_near:       #rewire 

                if passable(q_new, q_near, environment):
                        
                    current_cost = nodeTree.nodes[q_near].cost
                    new_cost = q_min_cost + cost(q_new, q_near, environment)

                    if new_cost < current_cost:
                        current_cost = new_cost
                        
                        print(f"change parent of {q_near} to {q_new}")
                        nodeTree.change_parent(q_near, q_new, cost(q_new, q_near, environment))
                    '''
                    if (q_near == end): 
                        #this should only happen once on the first connection of the end vertex
                        print("Found end")
                        found_path = True
                    '''

        if (iterations > 0):
            iterations = iterations - 1
        elif (found_path):
            break
    return True


def elevation_change_cost(start, end, environment):
    if start == end:
        return 0

    path = raytrace_nD(start, end)

    elev_cost = 0

    for i in range(1,len(path)):
        elev_cost += np.abs(int(environment[path[i]]) - int(environment[path[i-1]]))

    dist_cost= euclidean_distance(start, end)

    return dist_cost



def elevation_change_passable(start, end, threshold_single, threshold_total, environment):
    if start == end:
        return True

    path = raytrace_nD(start, end)

    elev_cost = 0

    i = 1
    while i < len(path):

        delta = np.abs(int(environment[path[i]]) - int(environment[path[i-1]]))
        if delta > threshold_single:
            return False
        
        elev_cost += delta
        i += 1

    if elev_cost > threshold_total * i:
        return False



    return True


def raytrace_nD(s, e):
    path = [s]
    start = np.asarray(s)
    end = np.asarray(e)
    delta = end-start 

    t = np.linalg.norm(delta)
    t_delta = np.where(delta != 0, t/delta, np.nan)

    step = np.sign(delta)
    t_max = t_delta/2
    pos = start

    while(not np.array_equal(pos, end)):

        dim = np.nanargmin(t_max)
        t_max[dim] += t_delta[dim]
        pos[dim] += step[dim]
        path = path + [tuple(pos)]

        #print(path)
        if np.linalg.norm(t_max) > t:
            break

    return path

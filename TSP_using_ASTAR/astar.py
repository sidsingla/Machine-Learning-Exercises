import math
import os, time
import heapq
import matplotlib.pyplot as plt


def create_graph(data):
    cities = int(data[0])
    graph = data[1: cities + 1]
    distances = {}
    vertices = []

    for node1 in graph:
        node1_info = node1.split(' ')
        vertex1, x1, y1 = node1_info
        vertices.append(vertex1)
        x1, y1 = int(x1), int(y1)
        distances[vertex1] = {}
        for node2 in graph:
            if node1 == node2:
                continue

            node2_info = node2.split(' ')
            vertex2, x2, y2 = node2_info
            x2, y2 = int(x2), int(y2)
            distances[vertex1][vertex2] = euclidean_dist( x1, y1, x2, y2 )
    return distances, vertices

def euclidean_dist( x1, y1, x2, y2 ):
    return math.sqrt( (x1-x2)**2 + (y1-y2)**2)

def minKey(keys, visited):
    min = 1e9
    min_index = 0

    for vertex in range(len(keys)):
        if keys[vertex] < min and not visited[vertex]:
            min = keys[vertex]
            min_index = vertex
    return min_index

def get_cost(parent, dist_graph, n):
    cost = 0
    for i in range(1, n):
        cost += dist_graph[i][parent[i]]

    return cost

def mst(vertices, dist_graph):
    n = len(vertices)
    keys = [ 1e9 for i in range(n) ]
    parent = {}
    keys[0] = 0
    visited = [False for i in range(n)]

    parent[0] = -1
    for i in range(n):
        a = minKey(keys, visited)

        visited[a] = True
        for b in range(n):
            if not visited[b] and dist_graph[a][b] > 0 and keys[b] > dist_graph[a][b]:
                keys[b] = dist_graph[a][b]
                parent[b] = a

    cost = get_cost(parent, dist_graph, n)
    return (cost)

def heuristic( unexplored_vertices, distances ):
    num_nodes = len( unexplored_vertices )
    if num_nodes == 1:
        return distances[unexplored_vertices[0]]['A']

    dist_graph = {}

    for i in range(num_nodes):
        dist_graph[i] = {}
        for j in range(num_nodes):
            if i == j:
                dist_graph[i][j] = 0
            else:
                dist_graph[i][j] = distances[ unexplored_vertices[i] ][ unexplored_vertices[j] ]

    return mst(unexplored_vertices, dist_graph)

def astar( distances, vertices ):
    if len(vertices) == 1:
        return 0, 0, 1

    start_time = time.time()
    n = len(vertices)
    start = vertices[0]
    generate = 0
    explored_set = []
    frontier = []
    heapq.heappush(frontier,(0, start))
    while True:
        if time.time() - start_time > 300:
            return None, -1, -1

        if len( frontier ) == 0:
            return None, -1, -1
        cost, path = heapq.heappop(frontier)

        if len(path) == len(vertices) + 1 and path[0] == start and path[-1] == start:
            return path, cost, generate

        explored_set.append( path )

        last_vertex = path[-1]

        if len(path) == len(vertices):
            generate += 1
            heapq.heappush(frontier, (cost + distances[last_vertex][start], path + start))
            continue

        unexplored_nodes = []
        for vertex in vertices:
            if vertex not in path:
                unexplored_nodes.append(vertex)

        for vertex in vertices:
            if vertex in path:
                continue
            generate += 1
            try:
                heuristic_cost = heuristic( unexplored_nodes, distances )
            except:
                heuristic_cost = 0
                pass
            fin_cost = cost + distances[last_vertex][vertex] + heuristic_cost
            heapq.heappush(frontier, (fin_cost, path + vertex))

city_count = {}
city_generations = {}

data_dir = 'tsp_problems'
for cities_dir in os.listdir(data_dir):
    city_count[int(cities_dir)] = 0
    city_generations[int(cities_dir)] = 0
    for instance in os.listdir(os.path.join(data_dir, cities_dir)):
        fil = open(os.path.join(data_dir + '/' + str(cities_dir) + '/', instance), 'r')

        st = fil.read()
        data = st.split('\n')

        distances, vertices = create_graph(data)
        #print ( distances, vertices )
        path, cost, generate = astar( distances, vertices )
        #print( path, cost, generate )
        if path is not None:
            city_count[int(cities_dir)] += 1
            city_generations[int(cities_dir)] += generate

    #print (cities_dir, city_generations)

for city, generations in city_generations.items():
    if generations != 0:
        city_generations[city] = city_generations[city]/city_count[city]


lists = sorted(city_generations.items()) # sorted by key, return a list of tuples
x, y = zip(*lists)

plt.figure()
plt.xlabel( 'No. of cities' )
plt.ylabel( 'Avg_Generations' )
plt.title( 'Cities vs average generations for TSP with heuristic' )
plt.style.use('seaborn-whitegrid')

import numpy as np
major_ticks = np.arange(0, 1000000, 5000)
plt.yticks(major_ticks)

plt.plot(x, y, '-o')
plt.show()

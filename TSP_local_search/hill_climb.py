import math
import os, time
import random
import pdb

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

def path_cost(path, distances):
    cost = 0
    for i in range(len(path)-1):
        cost += distances[path[i]][path[i+1]]
    return cost

def swap(i,j,path):
    path = list(path)
    path[i], path[j] = path[j], path[i]
    return ''.join(path)

def best_path(path, distances):
    best_cost = 1e9
    best_path = ""
    for i in range(1, len(path)-2):
        for j in range(i+1, len(path)-1):
            path = swap(i,j,path)
            cost = path_cost(path,distances)
            if cost < best_cost:
                best_cost = cost
                best_path = path
            path = swap(i,j,path)
    #print(best_path, best_cost)
    return best_path, best_cost

def get_random_path(vertices):
    path = "A"
    vertices_str = ""
    for vertex in vertices:
        if vertex == 'A':
            continue
        vertices_str += vertex

    str_var = list(vertices_str)
    random.shuffle(str_var)
    path += ''.join(str_var)
    path += 'A'
    return path

def hillclimb( distances, vertices ):
    curr_path = get_random_path(vertices)
    #print(curr_path)
    steps = 0
    curr_cost = path_cost(curr_path, distances)
    #print(curr_cost)

    while True:
        steps += 1
        path, best_neigh_cost = best_path(curr_path, distances)
        if best_neigh_cost < curr_cost:
            curr_cost = best_neigh_cost
            curr_path = path
        else:
            return curr_path, curr_cost, steps

# According to NEOS evaluator
best_cost = {}
best_cost['14'] = {}
best_cost['14']['instance_1.txt'] = 316.67
best_cost['14']['instance_2.txt'] = 324
best_cost['14']['instance_3.txt'] = 336
best_cost['14']['instance_4.txt'] = 319
best_cost['14']['instance_5.txt'] = 351
best_cost['14']['instance_6.txt'] = 311
best_cost['14']['instance_7.txt'] = 272
best_cost['14']['instance_8.txt'] = 361
best_cost['14']['instance_9.txt'] = 274
best_cost['14']['instance_10.txt'] = 322

best_cost['15'] = {}
best_cost['15']['instance_1.txt'] = 313
best_cost['15']['instance_2.txt'] = 318
best_cost['15']['instance_3.txt'] = 281
best_cost['15']['instance_4.txt'] = 324
best_cost['15']['instance_5.txt'] = 378
best_cost['15']['instance_6.txt'] = 291
best_cost['15']['instance_7.txt'] = 348
best_cost['15']['instance_8.txt'] = 342
best_cost['15']['instance_9.txt'] = 353
best_cost['15']['instance_10.txt'] = 325

best_cost['16'] = {}
best_cost['16']['instance_1.txt'] = 404
best_cost['16']['instance_2.txt'] = 353
best_cost['16']['instance_3.txt'] = 361
best_cost['16']['instance_4.txt'] = 349
best_cost['16']['instance_5.txt'] = 358
best_cost['16']['instance_6.txt'] = 344
best_cost['16']['instance_7.txt'] = 373
best_cost['16']['instance_8.txt'] = 355
best_cost['16']['instance_9.txt'] = 243
best_cost['16']['instance_10.txt'] = 330

if __name__ == "__main__":
    data_dir = 'tsp_problems'
    for cities_dir in os.listdir(data_dir):
        if int(cities_dir) > 16:
            continue
        city_step_avg = 0
        city_success_avg = 0
        city_soln_quality_avg = 0
        for instance in os.listdir(os.path.join(data_dir, cities_dir)):
            fil = open(os.path.join(data_dir + '/' + str(cities_dir) + '/', instance), 'r')
            st = fil.read()
            data = st.split('\n')
            distances, vertices = create_graph(data)
            total_steps = 0
            success = 0
            soln_quality_avg = 0
            #print(distances, vertices)
            for i in range(100):
                path, cost, steps = hillclimb( distances, vertices )
                total_steps += steps
                soln_quality_avg += cost/best_cost[str(cities_dir)][str(instance)]
                if cost <= best_cost[str(cities_dir)][str(instance)] * 1.01:
                    success += 1
                #print( steps, path, cost )
            print('cities', cities_dir, 'instance', instance)
            print('avg_steps', total_steps/100 )
            print('avg_solution_quality', soln_quality_avg/100)
            print('percentage_avg_success', success, 'cities', cities_dir, 'instance', instance)
            print('\n')
            city_step_avg += (total_steps/100)
            city_soln_quality_avg += (soln_quality_avg/100)
            city_success_avg += success

        print('...city_avg_steps...', city_step_avg/10, 'cities', cities_dir)
        print('...city_avg_solution_quality...', city_soln_quality_avg/10, 'cities', cities_dir)
        print('...city_avg_success...', city_success_avg/10, 'cities', cities_dir)
        print('\n')

import os, time, sys
import math
import random
import pdb
import hill_climb
import matplotlib.pyplot as plt


def get_neighbor( path ):
    i = random.randint(0, len(path)-1)
    j = random.randint(0, len(path)-1)
    path = hill_climb.swap(i,j,path)

    return path

def get_rand_path(vertices):
    path = ""
    random.shuffle(vertices)
    path += ''.join(vertices)
    return path

def get_cost(path, distances):
    cost = 0
    siz = len(path)
    for i in range(siz - 1):
        cost += distances[path[i]][path[i + 1]]
    cost += distances[path[siz-1]][path[0]]
    return cost

def get_new_T( algo, T, x ):
    if algo == 'linear':
        return T-1, 1

    if algo == 'log':
        x = x-1
        return math.log(x), x

    if algo == 'exp':
        return T*math.exp(-0.05), 1

def simulated_anneal( distances, vertices, algo, x=None ):
    T = 1e2
    curr_path = get_rand_path(vertices)
    curr_cost = get_cost(curr_path, distances)

    cou = 0
    while T > 1e-2:
        cou += 1
        neigh_path = get_neighbor(curr_path)

        try:
            neigh_cost = get_cost(neigh_path, distances)
        except:
            pass

        del_e = curr_cost - neigh_cost
        if del_e > 0:
            curr_path = neigh_path
            curr_cost = neigh_cost
        else:
            prob = math.exp(del_e/T)
            #print("prob ", prob)
            if random.random() <= prob:
                curr_path = neigh_path
                curr_cost = neigh_cost
        #print("T", T, "x", x)
        T, x = get_new_T(algo, T, x)
        #print(T)
    #print(cou, algo)
    return curr_path, curr_cost

data_dir = 'tsp_problems'
best_cost = {}
best_cost['14'] = {}
best_cost['14']['1'] = 316.67
best_cost['14']['2'] = 324
best_cost['15'] = {}
best_cost['15']['1'] = 313
best_cost['15']['2'] = 318
best_cost['16'] = {}
best_cost['16']['1'] = 404
best_cost['16']['2'] = 353


if __name__ == "__main__":

    algos = ['linear', 'log', 'exp']
    avg_sol = {}
    avg_time = {}

    for cities_dir in range(14,17):
        for inst in range(1,3):
            instance = 'instance_' + str(inst) + '.txt'
            city_inst = str(cities_dir) + '_' + str(instance)
            avg_sol[city_inst] = {}
            avg_time[city_inst] = {}

            fil = open(os.path.join(data_dir + '/' + str(cities_dir) + '/', instance), 'r')
            st = fil.read()
            data = st.split('\n')
            distances, vertices = hill_climb.create_graph(data)
            #print(distances, vertices)

            #print(cities_dir, instance)
            for algo in algos:
                avg_sol[city_inst][algo] = {}
                avg_time[city_inst][algo] = {}
                tot_soln_quality = 0
                tot_time = 0
                bestcost = best_cost[str(cities_dir)][str(inst)]
                for i in range(100):
                    start_time = time.time()
                    path, cost = simulated_anneal( distances, vertices, algo, x=1e4 )
                    tot_time += time.time() - start_time
                    #print(cost)
                    tot_soln_quality += cost / bestcost
                print(algo, cities_dir, inst, tot_soln_quality / 100)
                avg_sol[city_inst][algo] = tot_soln_quality / 100
                avg_time[city_inst][algo] = tot_time / 100

            '''
            plt.figure()
            plt.xlabel('Scheduling Algo')
            plt.ylabel('Average solution quality = Cost-LS/Cost-B')
            plt.title('Avg solution quality %s VS Scheduling algo')
            plt.style.use('seaborn-whitegrid')
            
            for city_inst in avg_sol.keys():
                lists = sorted(avg_sol[city_inst].items())  # sorted by key, return a list of tuples
                x, y = zip(*lists)
                plt.plot(x, y, '-o', label=city_inst)
            #plt.legend()
            '''
            plt.figure()
            plt.xlabel('Scheduling Algo')
            plt.ylabel('Average Execution Time')
            plt.title('Avg execution time VS Scheduling Algo')
            plt.style.use('seaborn-whitegrid')

            for city_inst in avg_time.keys():
                lists = sorted(avg_time[city_inst].items())  # sorted by key, return a list of tuples
                x, y = zip(*lists)
                plt.plot(x, y, '-o', label=city_inst)
            plt.legend()

    plt.show()

    #print(avg_sol)
    print(avg_time)
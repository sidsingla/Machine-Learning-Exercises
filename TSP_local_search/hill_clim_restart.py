import os, time
import random
import pdb
import hill_climb
import matplotlib.pyplot as plt

def hillclimb_random_restart( distances, vertices, best_cost, max_random_res ):
    iter = 0

    while True:
        iter += 1
        path, cost, _ = hill_climb.hillclimb(distances, vertices)
        #print(path, cost)
        if iter > max_random_res or cost <= best_cost * 1.01:
            return cost, path, iter

# According to NEOS evaluator
best_cost = {}
best_cost['14'] = {}
best_cost['14']['1'] = 316.67
best_cost['14']['2'] = 324
best_cost['15'] = {}
best_cost['15']['1'] = 313
best_cost['15']['2'] = 316
best_cost['16'] = {}
best_cost['16']['1'] = 404
best_cost['16']['2'] = 353

if __name__ == "__main__":
    avg_sol = {}
    avg_time = {}
    data_dir = 'tsp_problems'
    for cities_dir in range(14, 17):
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

            random_restarts = [i for i in range( 5, 72, 7) ]
            print(cities_dir, instance)
            #max_random_res = random.randint(1, 50)

            for random_restart in random_restarts:
                avg_sol[city_inst][random_restart] = {}
                avg_time[city_inst][random_restart] = {}
                tot_soln_quality = 0
                tot_time = 0
                bestcost = best_cost[str(cities_dir)][str(inst)]
                for i in range(100):
                    start_time = time.time()
                    cost, path, iter = hillclimb_random_restart( distances, vertices, bestcost, random_restart )
                    tot_time += time.time() - start_time
                    #print(cost, bestcost)
                    tot_soln_quality += cost/bestcost
                print(random_restart, cities_dir, inst, tot_soln_quality/100)
                avg_sol[city_inst][random_restart] = tot_soln_quality/100
                avg_time[city_inst][random_restart] = tot_time/100


    plt.figure()
    plt.xlabel( 'No. of Random Restarts' )
    plt.ylabel( 'Average solution quality = Cost-LS/Cost-B' )
    plt.title( 'Avg solution quality %s VS No. of restarts' )
    plt.style.use('seaborn-whitegrid')

    for city_inst in avg_sol.keys():
        lists = sorted(avg_sol[city_inst].items())  # sorted by key, return a list of tuples
        x, y = zip(*lists)
        #plt.legend([city_inst])
        plt.plot(x, y, '-o', label=city_inst)
    plt.legend()

    plt.figure()
    plt.xlabel('No. of Random Restarts')
    plt.ylabel('Average Execution Time')
    plt.title('Avg execution time VS No. of restarts')
    plt.style.use('seaborn-whitegrid')

    for city_inst in avg_time.keys():
        lists = sorted(avg_time[city_inst].items())  # sorted by key, return a list of tuples
        x, y = zip(*lists)
        #plt.legend([city_inst])
        plt.plot(x, y, '-o', label=city_inst)
    plt.legend()

    plt.show()

    print(avg_sol)
    print(avg_time)
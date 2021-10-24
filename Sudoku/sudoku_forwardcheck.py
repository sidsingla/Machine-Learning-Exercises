import os
import matplotlib.pyplot as plt

# Row constraint
def satisfy_row(row, column, x, mat):
    for i in range(len(mat[0])):
        if i == column:
            continue
        if mat[row][i] == x:
            return False
    return True

# Column constarint
def satisfy_column(row, column,x, mat):
    for i in range(len(mat)):
        if i == row:
            continue
        if mat[i][column] == x:
            return False
    return True

# Grid constraint
def satisfy_grid(row, column, x, mat):
    a = int(row/3) * 3
    b = int(column/3) * 3
    for i in range(a, a + 3):
        for j in range(b, b + 3):
            if i == row and j == column:
                continue
            if mat[i][j] == x:
                return False

    return True

def satisfy_constraints(row, column, x, mat):
    return satisfy_row(row, column, x, mat) and satisfy_column(row, column, x, mat) and satisfy_grid(row, column, x, mat)

def remove_values_from_domains(row, col, value, domains, n):
    # Removing value from domains of variables in same row.
    for i in range(n):
        try:
            if (str(row) + ' ' + str(i)) not in domains.keys():
                continue
            domains[str(row) + ' ' + str(i)].remove(value)
        except ValueError:
            pass

    # Removing value from domains of variables in same column.
    for i in range(n):
        try:
            if (str(i) + ' ' + str(col)) not in domains.keys():
                continue
            domains[str(i) + ' ' + str(col)].remove(value)
        except ValueError:
            pass

    # Removing value from domains of variables in same grid.
    a = int(row / 3) * 3
    b = int(col / 3) * 3
    for i in range(a, a + 3):
        for j in range(b, b + 3):
            try:
                if ( str(i) + ' ' + str(j) ) not in domains.keys():
                    continue

                domains[str(i) + ' ' + str(j)].remove(value)
            except ValueError:
                pass

    return domains

def get_domains( mat, n ):
    domains = {}
    for a in range(n):
        for b in range(n):
            if mat[a][b] != 0:
                continue
            domains[str(a) + ' ' + str(b)] = [i for i in range(1, 10)]

    for i in range(n):
        for j in range(n):
            if mat[i][j] != 0:
                # remove the value from other domains for csp
                domains = remove_values_from_domains(i, j, mat[i][j], domains, n)

            return domains

# Returns false when the domain of an assigned variable gets to zero because of assignment.
def forward_check(domains, mat, row, col, value, n):
    # Checking value from domains of variables in same row.
    for i in range(n):
        if mat[row][i] != 0:
            continue

        if len(domains[str(row) + ' ' + str(i)]) == 1 and domains[str(row) + ' ' + str(i)][0] == value:
                return False

    # Checking value from domains of variables in same column.
    for i in range(n):
        if mat[i][col] != 0:
            continue

        if len(domains[str(i) + ' ' + str(col)]) == 1 and domains[str(i) + ' ' + str(col)][0] == value:
            return False

    # Checking value from domains of variables in same grid.
    a = int(row / 3) * 3
    b = int(col / 3) * 3
    for i in range(a, a + 3):
        for j in range(b, b + 3):
            if mat[i][j] != 0:
                continue

            if len(domains[str(i) + ' ' + str(j)]) == 1 and domains[str(i) + ' ' + str(j)][0] == value:
                return False
    return True

def sudoku_fc(mat, n):
    global flag
    if flag == True:
        return False

    for i in range(n):
        for j in range(n):
            if mat[i][j] != 0:
                continue

            domains = get_domains(mat, n)

            # X[i][j] is the chosen variable
            for value in domains[str(i) + ' ' +  str(j)]:
                # Constraint check
                if satisfy_constraints(i,j,value,mat):
                    # Assign value to variable X[i][j]
                    mat[i][j] = value

                    global assignment
                    if assignment > 10000:
                        flag = True
                        return False
                    assignment += 1
                    domains[str(i) + ' ' +  str(j)].remove(value)
                    if forward_check(domains, mat, i, j, value, n):
                        if sudoku_fc(mat, n):
                            return True
                        if flag == True:
                            return False
                    mat[i][j] = 0
            return False
    return True

def get_initialisations(mat,n):
    count = 0
    for i in range(n):
        for j in range(n):
            if mat[i][j] != 0:
                count += 1
    return count

def create_matrix(data):
    data = data.replace(" ", "")
    data = data.splitlines()

    mat = []
    i = 0

    for st in data:
        row = []
        if st == '':
            continue
        for j in st:
            row.append(int(j))
        i += 1
        mat.append(row)
    return mat

data_dir = 'sudoku_problems'

initialisation_count = {}
initialisation_assignments = {}

for i in range(72):
    initialisation_count[i] = 0
    initialisation_assignments[i] = 0

for sudoku_dir in os.listdir(data_dir):
    print( "Running sudoku with backtracking and forward check on directory ", sudoku_dir )
    for instance in os.listdir(os.path.join(data_dir, sudoku_dir)):
        fil = open(os.path.join(data_dir + '/' + str(sudoku_dir) + '/', instance), 'r')
        data = fil.read()
        mat = create_matrix(data)
        n = len(mat)
        flag = False

        initialisations = get_initialisations(mat,n)
        assignment = 0
        sudoku_fc(mat, n)

        if flag == True:
            continue
        initialisation_count[initialisations] += 1
        initialisation_assignments[initialisations] += assignment
        #for row in mat:
            #print(row)

        #print ("Assignment count", assignment)

# key -> intialisations, value -> total assignments
print( "Total Assignment dict", initialisation_assignments )

# key -> intialisations, value -> count for instances with assignments <= 10000
print ("\nCount for which assignments < 10000", initialisation_count)

for i in range(72):
    if initialisation_count[i] == 0:
        initialisation_assignments[i] = 0
    else:
        initialisation_assignments[i] = initialisation_assignments[i]/initialisation_count[i]

# key -> intialisations, value -> Average assignments
print ("\nAverage assignments", initialisation_assignments)

lists = sorted(initialisation_assignments.items()) # sorted by key, return a list of tuples
x, y = zip(*lists)

plt.figure()
plt.xlabel( 'Initial values in matrix' )
plt.ylabel( 'Avg_Assignments' )
plt.title( 'Initialisations vs average assignments for sudoku with backtracking and forward-checking' )
plt.style.use('seaborn-whitegrid')

import numpy as np
major_ticks = np.arange(0, 11000, 100)
plt.yticks(major_ticks)

plt.plot(x, y, '-o')
plt.show()

print (initialisation_count)
print (initialisation_assignments)


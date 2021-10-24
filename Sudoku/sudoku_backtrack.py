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

# Column constraint
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

assignment = 0

def sudoku(mat):
    global flag
    if flag == True:
        return False

    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] != 0:
                continue

            for value in range(1, 10):
                if satisfy_constraints(i, j, value, mat):
                    mat[i][j] = value
                    global assignment
                    if assignment > 10000:
                        flag = True
                        return False
                    assignment = assignment + 1
                    if sudoku(mat):
                        return True

                    if flag == True:
                        return False
                mat[i][j] = 0
            return False
    return True

def get_intialisations(mat,n):
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
    print( "Running sudoku with backtracking on directory ", sudoku_dir)
    for instance in os.listdir(os.path.join(data_dir, sudoku_dir)):
        fil = open(os.path.join(data_dir + '/' + str(sudoku_dir) + '/', instance), 'r')

        data = fil.read()
        mat = create_matrix(data)
        n = len(mat)
        flag = False

        initialisations = get_intialisations(mat,n)
        assignment = 0
        sudoku(mat)

        if flag == True:
            continue
        initialisation_count[initialisations] += 1
        initialisation_assignments[initialisations] += assignment
        # for row in mat:
        # print(row)

        # print ("Assignment count", assignment)

# key -> intialisations, value -> total assignments
print( "Total Assignment dict", initialisation_assignments )

# key -> intialisations, value -> count for instances with assignments <= 10000
print ("\nCount for which assignments < 10000", initialisation_count)

for i in range(72):
    if initialisation_count[i] == 0:
        initialisation_assignments[i] = 0
    else:
        initialisation_assignments[i] = initialisation_assignments[i] / initialisation_count[i]


# key -> intialisations, value -> Average assignments
print( "\nAverage Assignments", initialisation_assignments )


lists = sorted(initialisation_assignments.items())  # sorted by key, return a list of tuples
x, y = zip(*lists)

plt.figure()
plt.xlabel('Initial values in matrix')
plt.ylabel('Avg_Assignments')
plt.title('Initialisations vs average assignments for sudoku with backtracking')
plt.style.use('seaborn-whitegrid')

import numpy as np
major_ticks = np.arange(0, 11000, 100)
plt.yticks(major_ticks)

plt.plot(x, y, '-o')
plt.show()

print(initialisation_count)
print(initialisation_assignments)

import pdb
import numpy as np
import math

# Matrix to store true utility values.
mat = np.zeros((3,4))

# Matrix to store true utility values in previous iteration.
mat_prev = np.zeros((3,4))

# Matrix to store optimal policies.
optimal_policies = np.chararray((3,4),itemsize=30)

# Matrix to store optimal policies in previous iteration.
optimal_policies_prev = np.chararray((3,4),itemsize=30)

optimal_policies[:] = ''
optimal_policies_prev[:] = ''

mat[1][3] = -1
mat[2][3] = 1
mat[1][1] = None

# Returns utility value of a state when an action is taken.
def left(i,j,mat):
    if j-1 >= 0 and math.isnan(mat[i][j-1]):
        return mat[i][j]

    if j-1 >= 0:
        return mat[i][j-1]
    else:
        return mat[i][j]

def right(i,j,mat):
    if j+1 < 4 and math.isnan(mat[i][j+1]):
        return mat[i][j]

    if j+1 < 4:
        return mat[i][j+1]
    else:
        return mat[i][j]

def up(i,j,mat):
    if i-1 >= 0 and math.isnan(mat[i-1][j]):
        return mat[i][j]

    if i-1 >= 0:
        return mat[i-1][j]
    else:
        return mat[i][j]

def down(i,j,mat):
    if i+1 < 3 and math.isnan(mat[i+1][j]):
        return mat[i][j]

    if i+1 < 3:
        return mat[i+1][j]
    else:
        return mat[i][j]

# Returns optimal policy action for a state.
def get_policy(policies):
    for action in policies.keys():
        count = 0
        optimal_policy = ""
        for other_action in policies.keys():
            if action == other_action:
                continue

            if policies[action] >= policies[other_action]:
                count += 1
                if optimal_policy == "":
                    optimal_policy += action
                if policies[action] == policies[other_action]:
                    optimal_policy += " " + other_action
            else:
                break

        if count == 3:
            li = optimal_policy.split()
            li.sort()
            return ' '.join(li)

    return ""

def algo( utility_fil, optimal_policy_fil, state_change_fil, reward_val ):
    utility_fil.write("Initial utility states\n")
    utility_fil.write(str(mat))

    for iteration in range(1, 11):
        # Making a copy of matrix before updating it.
        for i in range(3):
            for j in range(4):
                mat_prev[i][j] = mat[i][j]

        for i in range(3):
            for j in range(4):
                optimal_policies_prev[i][j] = optimal_policies[i][j]

        for i in range(3):
            for j in range(4):
                if math.isnan(mat[i][j]):
                    optimal_policies[i][j] = ""
                    continue
                if ( i == 1 and j == 3 ) or (i == 2 and j == 3):
                    optimal_policies[i][j] = ""
                    continue

                utility_up = up(i,j,mat_prev)
                utility_down = down(i, j, mat_prev)
                utility_right = right(i, j, mat_prev)
                utility_left = left(i, j, mat_prev)

                # Expected utility values for each action.
                expected_utility_up = 0.8 * utility_up + 0.1 * utility_left + 0.1 * utility_right
                expected_utility_left = 0.8 * utility_left + 0.1 * utility_up + 0.1 * utility_down
                expected_utility_right = 0.8 * utility_right + 0.1 * utility_up + 0.1 * utility_down
                expected_utility_down = 0.8 * utility_down + 0.1 * utility_left + 0.1 * utility_right

                expected_utility_policies = {}
                expected_utility_policies['up'] = expected_utility_up
                expected_utility_policies['left'] = expected_utility_left
                expected_utility_policies['right'] = expected_utility_right
                expected_utility_policies['down'] = expected_utility_down

                optimal_policies_cell = get_policy(expected_utility_policies)
                optimal_policy = optimal_policies_cell.split()[0]

                # Populating true utility value of the state
                mat[i][j] = reward_val + expected_utility_policies[optimal_policy]
                #Populating optimal policy of the state
                optimal_policies[i][j] = optimal_policies_cell
        #print("Printing matrix for iteration", iteration)
        #print(mat)
        state_change_fil.write("\nStates change for iteration " + str(iteration) + "\n")
        for i in range(3):
            for j in range(4):
                if optimal_policies[i][j] != optimal_policies_prev[i][j]:
                    state_change_fil.write("Optimal policy changes for state " + str(i) + " " + str(j))
                    state_change_fil.write("\n")

        utility_fil.write("\nPrinting utility matrix for iteration " + str(iteration) + "\n")
        utility_fil.write(str(mat))
        utility_fil.write("\n")

        optimal_policy_fil.write("\nPrinting optimal policy matrix for iteration " + str(iteration) + "\n")
        optimal_policy_fil.write(str(optimal_policies.decode("utf-8")))
        optimal_policy_fil.write("\n")

    utility_fil.close()
    optimal_policy_fil.close()
    state_change_fil.close()

if __name__ == '__main__':
    pass
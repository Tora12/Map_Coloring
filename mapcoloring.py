# Jenner Higgins
# CS 470
# Hill-Climbing, Min-Conflicts, Depth First Search
# WARNING: extremely messy code

from datetime import datetime
import pandas as pd
import numpy as np
import random
import sys
import copy

NUM_COLORS = 10 # solution for num_colors > 4
MAX_STEPS = 600000 # ~ 1 min

#params: copy of curr_solutions_list, conflict_index_list
def greedyNewSolution(s, index, num_assign):
    for i in range(len(index)):
        if(s[index[i]] == NUM_COLORS):
            s[index[i]] = 0
            num_assign += 1
        elif(s[index[i]] == (NUM_COLORS - 1)):
            s[index[i]] = s[index[i]] + 1
            num_assign += 1
        else:
            s[index[i]] = s[index[i]] + random.randint(1, 2)
            num_assign += 1
    return (s, num_assign)

def modifiedHillClimbing(m, r, c):
    counter = 0
    num_assign = 0
    curr_solutions = randomSolution(c)
    curr_conflicts, conflict_index = countConflicts2(m, curr_solutions, r, c)
    new_solutions = copy.deepcopy(curr_solutions)
    while(curr_conflicts != 0):
        if(counter > MAX_STEPS): # Most checks for a true is ~25
        # Most likely to happen when neighboring regions of x29
            return (False, num_assign, curr_conflicts)
        new_solutions, num_assign = greedyNewSolution(new_solutions, conflict_index, num_assign)
        new_conflicts, conflict_index,  = countConflicts2(m, new_solutions, r, c)
        if(new_conflicts < curr_conflicts):
            curr_solutions = new_solutions
            curr_conflicts = new_conflicts
            num_assign += 1
        counter += 1
    return (curr_solutions, num_assign, None)

#params: num_columns
def randomSolution(cols):
    solution = []
    for c in range(0, cols):
        random_color = random.randint(0, NUM_COLORS - 1) # colors start at 0
        solution.append(random_color)
    return solution

#params: curr_solution_list_copy, num_columns
def getNewSolution(s, c, num_assign):
    random_i = random.randint(0, c - 1)
    if(s[random_i] == NUM_COLORS):
        s[random_i] = 0
        num_assign += 1
    else:
        s[random_i] = s[random_i] + 1
        num_assign += 1
    return (s, num_assign)

#params: map_arr, num_rows, num_cols
def hillClimbing(map, rows, cols):
    counter = 0
    c = 0
    curr_solution = randomSolution(cols)
    curr_conflicts = countConflicts(map, curr_solution, rows, cols)
    new_solution = curr_solution # need deep copy?
    while(curr_conflicts != 0):
        if(counter > MAX_STEPS): # takes roughly a minute
            return (False, c, curr_conflicts)
        new_solutions, c = getNewSolution(new_solution, cols, c)
        new_conflicts = countConflicts(map, new_solution, rows, cols)
        if(new_conflicts < curr_conflicts):
            curr_solutions = new_solutions
            curr_conflicts = new_conflicts
            c += 1
        counter += 1
    return(curr_solution, c, None)

#params: map_list, solution_list, num_rows, num_columns
def countConflicts(m, s, rows, cols):
    conflicts = 0
    for r in range(0, rows):
    # r+2 b/c pandas adds its own row counter on top of xn counter in csv
        for c in range(r + 2, cols):
            if(m[r][c] == 1):
                if(s[r] == s[c] and s[r] != -1 and s[c] != -1):
                    conflicts += 1
    return conflicts

#params: conflict_list, conflict_location
def searchList(thislist, index):
    for i in thislist:
        if(i == index):
            return True
    return False

def countConflicts2(m, s, rows, cols):
    conflicts = 0
    index = []
    for r in range(0, rows):
    # r+2 b/c pandas adds its own row counter on top of xn counter in csv
        for c in range(r + 2, cols):
            if(m[r][c] == 1):
                #print(r, s[r], c, s[c])
                if(s[r] == s[c] and s[r] != -1 and s[c] != -1):
                    conflicts += 1
                    if(not searchList(index, c)):
                        index.append(c) # half of conflicts
                    elif(not searchList(index, r)):
                        index.append(r) # other half of conflicts
    return (conflicts, index)

def minConflicts(map, rows, cols): # bug?
    counter = 0
    curr_solution = randomSolution(cols)
    for i in range(0, 100000):
        curr_conflicts, conflict_index = countConflicts2(map, curr_solution, rows, cols)
        if(curr_conflicts == 0):
            return (curr_solution, counter, None)
        new_solution = curr_solution
        var = conflict_index[random.randint(0, len(conflict_index) - 1)]
        for j in range(0, NUM_COLORS):
            new_solution[var] = j
            temp_conflicts, temp_index = countConflicts2(map, curr_solution, rows, cols)
            if(temp_conflicts < curr_conflicts):
                curr_solution = new_solution
                counter += 1
    return(False, counter, None)

#param: solution_list
def fullyAssigned(s):
    for i in range(0, len(s)):
        if(s[i] == -1):
            return False
    return True

def normalDFS(map, solution, index, rows, cols, counter):
    for color in range(0, NUM_COLORS):
        new_solution = copy.deepcopy(solution)
        new_solution[index] = color
        counter += 1
        if(countConflicts(map, new_solution, rows, cols) == 0):
            if(fullyAssigned(new_solution) == True):
                return (True, new_solution, counter)
            else:
                temp, final_solution, counter = normalDFS(map, new_solution, index + 1, rows, cols, counter)
                if(temp == True):
                    return (True, final_solution, counter)
    return (False, None, counter)

def main():
    try:
        with open(sys.argv[1], 'r') as f:
            df = pd.read_csv(f)
    except:
        print("File error")

    # print(df.to_string()) # displays whole dataframe

    rows = df.shape[0]
    cols = df.shape[1]
    map = np.array(df.fillna(0))

    print("number of colors = ", NUM_COLORS)

    time = datetime.now()
    solution, counter, num_conflicts = hillClimbing(map, rows, cols)
    time = datetime.now() - time

    if(solution == False):
        print("Hill-climbing failed to find a solution in {} assignments with {} conflict(s) remaining ({}s)\n"
        .format(counter, num_conflicts, time))
    else:
        print("Hill-climbing found a solution in {}s and {} assignments:"
        .format(time, counter))
        print(solution, '\n')

    counter2 = 0
    time2 = datetime.now()
    solution2, counter2, num_conflicts2 = minConflicts(map, rows, cols)
    time2 = datetime.now() - time2
    if(solution2 == False):
        print("Min-conflicts failed to find a solution in {}s with {} assignments\n"
        .format(time2, counter2))
    else:
        print("Min-conflicts found a solution in {}s and {} assignments:".format(time2, counter2))
        print(solution2, '\n')

    solution3 = []
    for c in range(0, cols):
        solution3.append(-1)

    counter3 = 0
    time3 = datetime.now()
    temp, solution3, counter3 = normalDFS(map, solution3, 0, rows, cols, counter3)
    time3 = datetime.now() - time3

    if(temp == False):
        print("DFS failed to find a solution in {}s with {} assignments\n"
        .format(time3, counter3))
    else:
        print("DFS found a solution in {}s and {} assignments:".format(time3, counter3))
        print(solution3, '\n')

    time4 = datetime.now()
    solution4, counter4, num_conflicts4 = modifiedHillClimbing(map, rows, cols)
    time4 = datetime.now() - time4

    if(solution4 == False):
        print("Modified hill-climbing failed to find a solution in {} assignments with {} conflict(s) remaining ({}s)\n"
        .format(counter4, num_conflicts4, time4))
    else:
        print("Modified hill-climbing found a solution in {}s and {} assignments:"
        .format(time4, counter4))
        print(solution4, '\n')


if __name__ == "__main__":
    main()

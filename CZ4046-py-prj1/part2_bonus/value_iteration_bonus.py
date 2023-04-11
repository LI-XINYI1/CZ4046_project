from ctypes import util
import numpy as np
import copy
import sys
import csv
import os
from util.plot_img import plot_utility_iteration
import math


"""
Perform value iteration algorithm to base map

params
-epsilon: max error allowed in utility of any state, impacton convergence threshold

"""
def value_iteration_bonus():


    #create folder and file path to save the result 
    # 1. log_vi - epsilon value .txt  : save printouts in terminal to txt
    # 2. vi - epsion value .csv : save positions-iteration-utilities in .csv for plot
    rlt_path = os.path.join('part2_bonus/result-d999','value iteration')
    try:
        os.makedirs(rlt_path)
    except os.error:
        pass

    rlt_f = os.path.join(rlt_path,'vi.csv' )
    if os.path.exists(rlt_f):
        os.remove(rlt_f)

    log_f = os.path.join(rlt_path,'log_vi.txt' )
    if os.path.exists(log_f):
        os.remove(log_f)


    # direct the screen output to log.txt in a .txt file 
    # a reverting-back-to-outputting-to-screen code is at the end of the file
    stdoutOrigin = sys.stdout
    sys.stdout = open(log_f,"w")


    # information about the map
    # notice: epsilon is passed as a changing parameter to this function
    BOARD_ROWS = 10
    BOARD_COLS = 10
    GOOD_STATES = [(3, 2),(0,1),(0,2),(1,1),(9, 6),(9,7)]
    BAD_STATES = [(1, 5),(1, 9),(2,9),(5, 9),(7, 2)]
    START = (6, 6)
    WALLS = [(3, 8),(4, 8),(5, 8),(6, 8),(7, 8),(7,5),(8,5),(9,5)]
    epsilon = 1
    #factors in value iteration
    GAMMA = 0.999
    NT_REWARDS = -0.04    #reward value for non terminal states 
    Converg_Threshold = epsilon * (1-GAMMA)/GAMMA
    
    # actions of agent
    NUM_OF_ACTIONS = 4
    ACTIONS = [(-1,0),(0,-1),(1,0),(0,1)]   #Up Left Down Right



    # initialize the map
    map_states = [[0] * BOARD_COLS for i in range(BOARD_ROWS)]

    for state in GOOD_STATES:
        map_states[state[0]][state[1]] = 10

    for state in BAD_STATES:
        map_states[state[0]][state[1]] = -1


    """
    get the utility of given action in the state

    params
    - states: a BOARD_ROWS * BOARD_COLS size matrix stores utilities 
    - row: row index of target grid
    - col: column index of target grid
    - action: an integer from [0,3], denoting [Up, Left, Down, Right]

    return:(
        {utility of the state after performing required actions}
    )
    """
    def get_utility(states, row, col, action):      
        temp_row = row + ACTIONS[action][0]
        temp_col = col + ACTIONS[action][1]
        if temp_row < 0 or temp_row >= BOARD_ROWS or temp_col < 0 or temp_col >= BOARD_COLS \
            or (temp_row, temp_col) in WALLS:
            return states[row][col]
        else:
            return states[temp_row][temp_col]

    """
    Get the expected utility of the stated after taking actions
    Using BELLMAN EQUATION

    params:
    - states: a BOARD_ROWS * BOARD_COLS size matrix stores utilities
    - row: row index of target grid
    - col: column index of target grid
    - action: an integer from [0,3], denoting [Up, Left, Down, Right]

    return:(
        utility: the updated utility calculated by 
    )
    """
    def evaluate_utility(states, row, col, action):    
        utility = NT_REWARDS
        if (row, col) in GOOD_STATES:
            utility = 1
        elif (row, col) in BAD_STATES:
            utility = -1
        utility += 0.1 * get_utility(states,row,col,(action-1)%4)
        utility += 0.1 * get_utility(states,row,col,(action+1)%4)
        utility += 0.8 * get_utility(states,row,col,(action))

        return GAMMA*utility
        
    """
    Get the optimal move for the agent in current state and utility value

    params:
    - states: a BOARD_ROWS * BOARD_COLS size matrix stores utilities 

    return:(
        policy: the optimal action for each state
    )
    """
    def get_policy(states):   #find the best move the AI can take at that state
        policy = [[None] * BOARD_COLS for i in range(BOARD_ROWS)]
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                best_action = -math.inf
                best_utility = -math.inf
                for action in range(NUM_OF_ACTIONS):
                    utility = evaluate_utility(states, row, col, action)
                    if utility > best_utility: 
                        best_utility = utility
                        best_action = action
                policy[row][col] = best_action

        return policy
    
    # function to print policy
    def print_policy(matrix):   
        for row in range(BOARD_ROWS):
            print("|",end="")
            for col in range(BOARD_COLS):
                if (row, col) in WALLS:
                    print("  W   ", end=" | ")
                elif (row, col) in GOOD_STATES:
                    if matrix[row][col] == 0:
                        print(" G (^)", end=" | ")
                    elif matrix[row][col] == 1:
                        print(" G (<)", end=" | ")
                    elif matrix[row][col] == 2:
                        print(" G (v)", end=" | ")
                    elif matrix[row][col] == 3:
                        print(" G (>)", end=" | ")
                elif (row, col) in BAD_STATES:
                    if matrix[row][col] == 0:
                        print(" B (^)", end=" | ")
                    elif matrix[row][col] == 1:
                        print(" B (<)", end=" | ")
                    elif matrix[row][col] == 2:
                        print(" B (v)", end=" | ")
                    elif matrix[row][col] == 3:
                        print(" B (>)", end=" | ")
                else:
                    if matrix[row][col] == 0:
                        print("  ^   ", end=" | ")
                    elif matrix[row][col] == 1:
                        print("  <   ", end=" | ")
                    elif matrix[row][col] == 2:
                        print("  v   ", end=" | ")
                    elif matrix[row][col] == 3:
                        print("  >   ", end=" | ")
            print()           
    

    def print_states(matrix):
        for row in range(BOARD_ROWS):
            print("|",end="")
            for col in range(BOARD_COLS):
                if (row, col) in WALLS:
                    print(" WALL ", end=" | ")
                else:
                    print(str(matrix[row][col])[:6], end=" | ")
            print()

    """
    Calculate the value of each state

    params:
    -states: a BOARD_ROWS * BOARD_COLS size matrix stores utilities initialized as 0

    return:(
        updated utility value of given states with optimal actions
    )
    """
    def value_iteration(states):     

        with open(rlt_f,'a',newline='') as file:
            
            writer = csv.writer(file)

            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    writer.writerow([f"({row},{col})", 0, 0])
            
            iteration = 1
            while True: 
                print("Iteration " , iteration)
                next_state = copy.deepcopy(states)   
                max_diff = 0
                for row in range(BOARD_ROWS):
                    for col in range(BOARD_COLS):
                        utilities = []
                        for action in range(NUM_OF_ACTIONS):
                            utilities.append(evaluate_utility(states, row, col, action))

                        next_state[row][col] = max(utilities)
                        max_diff = max(max_diff,abs(next_state[row][col]-states[row][col]))  

                        writer.writerow([f"({row},{col})", iteration, next_state[row][col]])
                
                states = next_state
                print_states(states)

                #stop iterating once max_diff between previous iteration and current iteration < epsilon
                if max_diff < Converg_Threshold:    
                    break
                iteration += 1

        return states


    #print out the initial map
    print("Displaying the Map")
    print("\n")
    print_states(map_states)
    print("\n")

    #perform value iteration and derive the optimal policy
    map_states = value_iteration(map_states)
    best_policy = get_policy(map_states)
    print("\n")
    print("***************Best Policy*********************")
    print_policy(best_policy)


    # reverting-back-to-outputting-to-screen code 
    # close log.txt
    # printouts in terminal as original setting
    sys.stdout.close()
    sys.stdout=stdoutOrigin

    # call plot_utility_iteration to plot the image
    plot_utility_iteration(2,"v",1,9,9)

from ctypes import util
import numpy as np
import copy
import sys
import csv
import random
import os
from util.plot_img import plot_utility_iteration
import math

"""
Perform policy iteration algorithm to base map

"""
def policy_iteration():


    #create folder and file path to save the result 
    # 1. log_pi - epsilon value .txt  : save printouts in terminal to txt
    # 2. pi - epsion value .csv : save positions-iteration-action-utilities in .csv for plot
  
    rlt_path = os.path.join('part1/result','policy iteration')
    try:
        os.makedirs(rlt_path)
    except os.error:
        pass

    rlt_f = os.path.join(rlt_path,'pi.csv' )
    if os.path.exists(rlt_f):
        os.remove(rlt_f)

    log_f = os.path.join(rlt_path,'log_pi.txt')
    if os.path.exists(log_f):
        os.remove(log_f)


    # direct the screen output to log.txt in folder rlt
    # a reverting-back-to-outputting-to-screen code is at the end of the file
    stdoutOrigin = sys.stdout
    sys.stdout = open(log_f,"w")


   # information about the map
    # notice: epsilon is passed as a changing parameter to this function
    BOARD_ROWS = 6
    BOARD_COLS = 6
    GOOD_STATES = [(0, 0),(0, 2),(0, 5),(1, 3),(2, 4),(3, 4)]
    BAD_STATES = [(1, 1),(2, 2),(3, 3),(4, 4),(1, 5)]
    START = (3, 2)
    WALLS = [(0, 1),(1, 4),(4, 1),(4, 2),(4, 3)]
   
    #factors in value iteration
    GAMMA = 0.99
    EPSILON = 10**(-6)
    NT_REWARDS = -0.04    
    Converg_Threshold = EPSILON * (1-GAMMA)/GAMMA
    
    # actions of agent
    NUM_OF_ACTIONS = 4
    ACTIONS = [(-1,0),(0,-1),(1,0),(0,1)]   #Up Left Down Right


    # initialize the map
    map_states = [[0] * BOARD_COLS for i in range(BOARD_ROWS)]

    for state in GOOD_STATES:
        map_states[state[0]][state[1]] = 1   

    for state in BAD_STATES:
        map_states[state[0]][state[1]] = -1

    policy = [[random.randint(0,3) for j in range(BOARD_COLS)] for j in range(BOARD_ROWS)]  #initialise all the policies randomly 



    def get_policy(states):  
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
        
    def print_policy(matrix):  
        for row in range(BOARD_ROWS):
            print("|",end="")
            for col in range(BOARD_COLS):
                if (row, col) in WALLS:
                    print(" WALL ", end=" | ")
                elif (row, col) in GOOD_STATES:
                    if matrix[row][col] == 0:
                        print("+1 (^)", end=" | ")
                    elif matrix[row][col] == 1:
                        print("+1 (<)", end=" | ")
                    elif matrix[row][col] == 2:
                        print("+1 (v)", end=" | ")
                    elif matrix[row][col] == 3:
                        print("+1 (>)", end=" | ")
                elif (row, col) in BAD_STATES:
                    if matrix[row][col] == 0:
                        print("-1 (^)", end=" | ")
                    elif matrix[row][col] == 1:
                        print("-1 (<)", end=" | ")
                    elif matrix[row][col] == 2:
                        print("-1 (v)", end=" | ")
                    elif matrix[row][col] == 3:
                        print("-1 (>)", end=" | ")
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
                elif(row,col) in GOOD_STATES:
                    print("   1  ", end=" | ")
                elif(row,col) in BAD_STATES:
                    print("  -1  ", end=" | ")
                else:
                    print(str(matrix[row][col])[:6], end=" | ")

            print()

    def print_utilities(matrix):
        for row in range(BOARD_ROWS):
            print("|",end="")
            for col in range(BOARD_COLS):
                if (row, col) in WALLS:
                    print(" WALL ", end=" | ")
                else:
                    print(str(matrix[row][col])[:6], end=" | ")

            print()

    def get_utility(states, row, col, action):     
        temp_row = row + ACTIONS[action][0]
        temp_col = col + ACTIONS[action][1]
        if temp_row < 0 or temp_row >= BOARD_ROWS or temp_col < 0 or temp_col >= BOARD_COLS \
            or (temp_row, temp_col) in WALLS:
            return states[row][col]
        else:
            return states[temp_row][temp_col]


    def evaluate_utility(states, row, col, action):   
        utility = NT_REWARDS
    
        if (row, col) in GOOD_STATES:
            utility = 1
        elif (row, col) in BAD_STATES:
            utility = -1
        utility += 0.1 * (GAMMA * get_utility(states,row,col,(action-1)%4))
        utility += 0.1 * (GAMMA * get_utility(states,row,col,(action+1)%4))
        utility += 0.8 * (GAMMA * get_utility(states,row,col,(action)))

        return utility

    def policy_making(policy, states):   
        max_diff = 0
        while True:
            next_state = copy.deepcopy(states)    
            max_diff = 0
            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    next_state[row][col] = evaluate_utility(states, row, col, policy[row][col])
                    max_diff = max(max_diff, abs(next_state[row][col] - states[row][col]))  
                                                                                           
            states = next_state
            #print("change")
            if max_diff < Converg_Threshold:   
                break
        return states

    def policy_iteration(policy, state):     
        iteration = 1
        while True:
            state = policy_making(policy, state)       
            modified = 0    

            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    best_action = None
                    best_utility = -float("inf")
                    for action in range(NUM_OF_ACTIONS):
                        ut = evaluate_utility(state, row, col, action)   
                        if ut > best_utility:
                            best_action = action     
                            best_utility = ut      
                        
                    if best_utility > evaluate_utility(state , row, col, policy[row][col]):   
                        policy[row][col] = best_action
                        modified = 1   

            with open(rlt_f, 'a', newline='') as file:
                writer = csv.writer(file)
                for row in range(BOARD_ROWS):
                    for col in range(BOARD_COLS):
                        writer.writerow([f"({row},{col})", iteration, policy[row][col], state[row][col]])

            print("Iteration ", iteration)
            print_policy(policy)
            print()
            
            if modified == 0:  
                break
            iteration += 1

        return policy, state
    
                    

    print("\n")

    policy, map_states = policy_iteration(policy, map_states)
    best_policy = get_policy(map_states)
    print("\n")
    print("Displaying the Map")
    print("\n")
    print_utilities(map_states)
    print("\n")
    print("***************Best Policy*********************")
    print("\n")
    print_policy(policy)


    sys.stdout.close()
    sys.stdout=stdoutOrigin

    plot_utility_iteration(1,"p")


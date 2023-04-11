from part1.value_iteration import value_iteration
from part1.policy_iteration import policy_iteration
from part2_bonus.value_iteration_bonus import value_iteration_bonus
from part2_bonus.value_iteration_bonus_large import value_iteration_bonus_large
from part2_bonus.policy_iteration_bonus import policy_iteration_bonus


if __name__ == '__main__':
    
    """
    This is the main function of MDP
    By running this main.py, it will consecutively run value_iteration with 3 different EPSILONs
        and policy_iteration, for part 1 base maze
    Next, it will run for the designed complex maze.

    Notice that all the printouts in terminal are saved in result/value_or_policy iteration/log_vi or log_pi.txt
    Please find the plots and result policy maze in corresponding results folder. 
    """

    value_iteration(10**(-6))
    value_iteration(1)
    value_iteration(10)
    policy_iteration()

    """
    The file path and value setting for current value_iteration_bonus() and policy_iteration_bonus() and util/plot_utility_iteration()
    are set for GAMMA=0.999.
    """
    value_iteration_bonus()
    policy_iteration_bonus()
    value_iteration_bonus_large()

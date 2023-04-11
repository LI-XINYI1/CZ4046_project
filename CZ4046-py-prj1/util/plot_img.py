import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


"""
Plot utilityutility estimates as a function of the number of iterations

params:
-part_index: 1 : part 1, 2: bonus
-policy_index: "v": value iteration, "p":policy iteration
-colsize: num of columns of maze, default 5 for base maze
-rowsize: num of rows of maze, default 5 for base maze

"""
def plot_utility_iteration(part_index, policy_index,epsilon=0,colsize=5,rowsize=5):
    path = os.getcwd()

    def organize_grid_df(policy_index,position):
        if policy_index == 0:
            value_state_df = value_df.loc[position]
            return value_state_df
        else:
            policy_state_df = policy_df.loc[position]
            return policy_state_df

    if part_index == 1:
        if policy_index == "v":
            vi_rlt_path = os.path.join(path,'part1/result','value iteration','vi - '+str(epsilon))
            vi_data_path = os.path.join(vi_rlt_path,'vi - '+str(epsilon) +'.csv')
            try:
                os.makedirs(vi_rlt_path)
            except os.error:
                pass
            vi_img_path = os.path.join(vi_rlt_path,'vi - utility -'+str(epsilon)+'.png')
            value_headers = ['Position', 'Iteration', 'Utility']


            ##############改
            value_df = pd.read_csv(vi_data_path,header=None, names=value_headers)
            value_df = value_df.astype({"Position":"string"})

            positions = []
            for x in range(0,colsize+1):
                for y in range(0,rowsize+1):
                    pos_key = ",".join(str(x)+str(y))
                    pos_key="("+pos_key +")"
                    positions.append(pos_key)
                    pos_key =""

            value_df.set_index('Position',inplace=True)

            figure(figsize=(16, 8))

            for x in positions:
                value_state_df = organize_grid_df(0,x)
                plt.plot(value_state_df['Iteration'], value_state_df['Utility'], label=x)
            plt.title("Value Iteration - Utility -" +str(epsilon)+" (part1)")
            plt.xlabel("Iterations")
            plt.ylabel("Utility Values")
            plt.legend(loc=2, prop={'size': 6})
            plt.savefig(vi_img_path)
            plt.show()
        

        if policy_index == "p":
            pi_rlt_path = os.path.join(path,'part1/result','policy iteration')
            try:
                os.makedirs(pi_rlt_path)
            except os.error:
                pass

            pi_img_path = os.path.join(pi_rlt_path,'policy iteration - utility.png')
            policy_headers = ['Position', 'Iteration', 'Action', 'Utility']
            pi_data_path = os.path.join(pi_rlt_path,'pi.csv')

            #########
            policy_df = pd.read_csv(pi_data_path,header=None, names=policy_headers)
            policy_df = policy_df.astype({"Position":"string"})


            positions = []
            for x in range(0,colsize+1):
                for y in range(0,rowsize+1):
                    pos_key = ",".join(str(x)+str(y))
                    pos_key="("+pos_key +")"
                    positions.append(pos_key)
                    pos_key =""

            policy_df.set_index('Position',inplace=True)

            figure(figsize=(16, 8))

            for x in positions:
                #if x=="" 删除walls的
                policy_state_df = organize_grid_df(1,x)
                plt.plot(policy_state_df['Iteration'], policy_state_df['Utility'], label=x)
            plt.title("Policy Iteration - Utility (part1)")
            plt.xlabel("Iterations")
            plt.ylabel("Utility")
            plt.legend(loc=2, prop={'size': colsize+1})
            plt.savefig(pi_img_path)
            plt.show()

    elif part_index == 2:
        if policy_index == "v":
            vi_rlt_path = os.path.join(path,'part2_bonus/result-d999','value iteration')
            vi_data_path = os.path.join(vi_rlt_path,'vi.csv')
            try:
                os.makedirs(vi_rlt_path)
            except os.error:
                pass
            vi_img_path = os.path.join(vi_rlt_path,'vi - utility.png')
            value_headers = ['Position', 'Iteration', 'Utility']


            value_df = pd.read_csv(vi_data_path,header=None, names=value_headers)
            value_df = value_df.astype({"Position":"string"})

            positions = []
            for x in range(0,colsize+1):
                for y in range(0,rowsize+1):
                    pos_key = ",".join(str(x)+str(y))
                    pos_key="("+pos_key +")"
                    positions.append(pos_key)
                    pos_key =""

            value_df.set_index('Position',inplace=True)

            figure(figsize=(16, 8))

            for x in positions:
                value_state_df = organize_grid_df(0,x)
                plt.plot(value_state_df['Iteration'], value_state_df['Utility'], label=x)
            plt.title("Value Iteration - Utility  (part2)")
            plt.xlabel("Iterations")
            plt.ylabel("Utility Values")
            plt.legend(loc=2, prop={'size': colsize+1})
            plt.savefig(vi_img_path)
            plt.show()
        
        if policy_index == "p":
            pi_rlt_path = os.path.join(path,'part2_bonus/result-d999','policy iteration')
            try:
                os.makedirs(pi_rlt_path)
            except os.error:
                pass

            pi_img_path = os.path.join(pi_rlt_path,'policy iteration - utility.png')
            policy_headers = ['Position', 'Iteration', 'Action', 'Utility']
            pi_data_path = os.path.join(pi_rlt_path,'pi.csv')

            #########
            policy_df = pd.read_csv(pi_data_path,header=None, names=policy_headers)
            policy_df = policy_df.astype({"Position":"string"})


            positions = []
            for x in range(0,colsize+1):
                for y in range(0,rowsize+1):
                    pos_key = ",".join(str(x)+str(y))
                    pos_key="("+pos_key +")"
                    positions.append(pos_key)
                    pos_key =""

            policy_df.set_index('Position',inplace=True)

            figure(figsize=(16, 8))

            for x in positions:
                policy_state_df = organize_grid_df(1,x)
                plt.plot(policy_state_df['Iteration'], policy_state_df['Utility'], label=x)
            plt.title("Policy Iteration - Utility (part2)")
            plt.xlabel("Iterations")
            plt.ylabel("Utility")
            plt.legend(loc=2, prop={'size': colsize+1})
            plt.savefig(pi_img_path)
            plt.show()
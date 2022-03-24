import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from BlackJack import BlackJackTable

# Helper function for integrating CSV-file with BlackJackTable Card format
def replace_card_with_csv(card):
    return {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "JACK": 10,
            "QUEEN": 10, "KING": 10, "ACE": "ACE"}[card]

def pandas_helper(x):
    if x == 0:
        return "Push"
    elif x > 0:
        return "Win"
    else:
        return "Lose"

loop = False #T/F
num_iterations = 100
it = 0

# Determine starting values
origin_money = 10000
stake = 100
simulation_rounds = 10000

if loop == False:

    if __name__ == '__main__':
        bjt = BlackJackTable()
    
        '''
        Include all strats here
        
        Excel-Files have to be in the following format:
        - Include Header with Dealer values
        - The index-column has to be in a specific order, as the options are check row-wise
            -> First write all combinations with , seperated (no space before or after ,)
        
        strat1.csv as reference
        '''
        strats = []
        strats.append(pd.read_csv('strat1.csv', sep=";", header=0, index_col=0))
        strats.append(pd.read_csv('strat2.csv', sep=";", header=0, index_col=0))
        strats.append(pd.read_csv('strat3.csv', sep=";", header=0, index_col=0))
        strats.append(pd.read_csv('strat4.csv', sep=";", header=0, index_col=0))
        strats.append(pd.read_csv('strat5.csv', sep=";", header=0, index_col=0))
        strats.append(pd.read_csv('strat6.csv', sep=";", header=0, index_col=0))
    
        data = {
            "Hands Played": [], "strat": [],
            "dealer": [],
            "player": [],
            "return": [],
            "total": []}
        df_returns = pd.DataFrame(data)
    
    
    
        # Execute for each strategy
        for strat in range(len(strats)):
            # Reset money for each strategy
            money = origin_money
            for game_round in range(simulation_rounds):
                while not bjt.is_finished():
                    # Get the game state and determine dealers card
                    game_state = bjt.get_game_state()
                    column = strats[strat][str(replace_card_with_csv(game_state['dealer'][0]))]
                    actions = []
    
                    # Find the action for each hand being played
                    for hand_index, hand in enumerate(game_state['player']):
                        # If the hand is already terminated, append Nothing and continue with next hand
                        if game_state['player'][hand_index][-1] == "TERMINATED":
                            actions.append("Nothing")
                            continue
    
                        # Get the value of the deck
                        value_to_take = bjt.get_final_value_of_deck(game_state['player'][hand_index])
                        for action_index, action in column.items():
                            # See if there is a combination in the strategy that fits the current hand
                            if "," in action_index and len(game_state['player'][hand_index]) == 2:
                                if (str(game_state['player'][hand_index][0]) == str(action_index.split(",")[0]) and str(
                                        game_state['player'][hand_index][1]) == str(action_index.split(",")[1])) or (
                                        str(game_state['player'][hand_index][0]) == str(
                                    action_index.split(",")[1]) and str(game_state['player'][hand_index][1]) == str(
                                    action_index.split(",")[0])):
                                    actions.append(action)
                                    break
                            else:
                                # Else just look at the value and determine action
                                if str(action_index) == str(value_to_take):
                                    actions.append(action)
                                    break
    
                    bjt.do_action(actions)
    
                # Apply the return to your current money pool
                money += stake * bjt.get_return()
                # Comment out if plotting win percentage by initial dealer/player card values
                # if money <= 0:
                #     money = 0
                #     df_returns = df_returns.append(
                #     {"Hands Played": game_round, "strat": f"Strategy {strat+1}", "dealer": bjt.get_game_state()['player'],
                #       'player': bjt.get_game_state()['player'], 'return': stake * bjt.get_return(), 'total': money},
                #     ignore_index=True)
                #     break
                
                # Write the data to the dataframe for later analysis
                df_returns = df_returns.append(
                    {"Hands Played": game_round, "strat": f"Strategy {strat+1}", "dealer": bjt.get_game_state()['dealer'],
                     'player': bjt.get_game_state()['player'], 'return': stake * bjt.get_return(), 'total': money},
                    ignore_index=True)
    
                # Reset BlackJackTable
                bjt.reset_table()
                
        df_returns['total'] = df_returns['total'].fillna(0)
        
        # Draw a plot showing the percentage of push or win for each dealers value possible
        # sns.lineplot(x=[bjt.get_final_value_of_deck([x[0]]) for x in df_returns["dealer"]], y=df_returns["return"]>=0, hue=df_returns["strat"], ci=None).set(title="Percentage for a win or push by dealers value")
        # plt.show()
    
        # # Draw a plot showing the percentage of push or win for each players value possible
        # sns.lineplot(x=[int(bjt.get_final_value_of_deck(x[0][0:2])) for x in df_returns["player"]], y=df_returns["return"] >= 0, hue = df_returns["strat"],ci=None).set(title="Percentage for a win or push by players initial hand value")
        # plt.show()
    
        # Draw a pie chart for each strategy showing the distribution fo Win, Push and Lose
        # for strat in range(len(strats)):
        #     df_data = df_returns[df_returns["strat"] == "Strategy "+str(strat+1)]
        #     plt.pie([len(df_data[df_data["return"]>0]), len(df_data[df_data["return"]==0]),len(df_data[df_data["return"]<0])], labels=["Win", "Push", "Lose"])
        #     plt.title('Distribution of game outcome for strategy '+str(strat+1))
        #     plt.show()
        
        # Draw a bar chart for each strategy 
        labels=["Win", "Push", "Lose"]
        x_pos = [i for i, _ in enumerate(labels)]
        for strat in range(len(strats)):
            df_data = df_returns[df_returns["strat"] == "Strategy "+str(strat+1)]
            y = [len(df_data[df_data["return"]>0])/len(df_data), len(df_data[df_data["return"]==0])/len(df_data),len(df_data[df_data["return"]<0])/len(df_data)]
            y = list(np.around(np.array(y),5))
            plt.bar(x_pos, y, color = ['green', 'blue', 'red'])
            plt.title('Distribution of game outcome for strategy '+str(strat+1))
            plt.xticks(x_pos, labels)
            plt.legend(loc='lower right')
            plt.text(-0.15, 0.3,y[0])
            plt.text(0.8, 0.3,y[1])
            plt.text(1.8, 0.3,y[2])
            plt.show()
    
        df_returns['Profit'] = df_returns['total'] - 10000
        # Draw a plot showing the money for each strategy
        sns.lineplot(data=df_returns, x="Hands Played", y='Profit', hue="strat").set(title="Money trend for strategies")
        plt.show()

#play entire games thousands of times
if loop == True:
    
    if __name__ == '__main__':
        bjt = BlackJackTable()
    
        '''
        Include all strats here
        
        Excel-Files have to be in the following format:
        - Include Header with Dealer values
        - The index-column has to be in a specific order, as the options are check row-wise
            -> First write all combinations with , seperated (no space before or after ,)
        
        strat1.csv as reference
        '''
        strats = []
        strats.append(pd.read_csv('strat1.csv', sep=";", header=0, index_col=0))
        strats.append(pd.read_csv('strat2.csv', sep=";", header=0, index_col=0))
        strats.append(pd.read_csv('strat3.csv', sep=";", header=0, index_col=0))
        strats.append(pd.read_csv('strat4.csv', sep=";", header=0, index_col=0))
        strats.append(pd.read_csv('strat5.csv', sep=";", header=0, index_col=0))
        strats.append(pd.read_csv('strat6.csv', sep=";", header=0, index_col=0))
    
    
        data = {
            "Hands Played": [], "strat": [],
            "dealer": [],
            "player": [],
            "return": [],
            "total": []}        
        df_returns = pd.DataFrame(data)
        
        sim_data = {
            "strat": [], "total hands played": [],
            "ending profit": [],
            "win %": [],
            "push %": [],
            "loss %": []
            }
        df_loop_sim = pd.DataFrame(sim_data)
    
    
        for i in range(num_iterations):
            # Execute for each strategy
            for strat in range(len(strats)):
                # Reset money for each strategy
                money = origin_money
                for game_round in range(simulation_rounds):
                    while not bjt.is_finished():
                        # Get the game state and determine dealers card
                        game_state = bjt.get_game_state()
                        column = strats[strat][str(replace_card_with_csv(game_state['dealer'][0]))]
                        actions = []
        
                        # Find the action for each hand being played
                        for hand_index, hand in enumerate(game_state['player']):
                            # If the hand is already terminated, append Nothing and continue with next hand
                            if game_state['player'][hand_index][-1] == "TERMINATED":
                                actions.append("Nothing")
                                continue
        
                            # Get the value of the deck
                            value_to_take = bjt.get_final_value_of_deck(game_state['player'][hand_index])
                            for action_index, action in column.items():
                                # See if there is a combination in the strategy that fits the current hand
                                if "," in action_index and len(game_state['player'][hand_index]) == 2:
                                    if (str(game_state['player'][hand_index][0]) == str(action_index.split(",")[0]) and str(
                                            game_state['player'][hand_index][1]) == str(action_index.split(",")[1])) or (
                                            str(game_state['player'][hand_index][0]) == str(
                                        action_index.split(",")[1]) and str(game_state['player'][hand_index][1]) == str(
                                        action_index.split(",")[0])):
                                        actions.append(action)
                                        break
                                else:
                                    # Else just look at the value and determine action
                                    if str(action_index) == str(value_to_take):
                                        actions.append(action)
                                        break
        
                        bjt.do_action(actions)
        
                    # Apply the return to your current money pool
                    money += stake * bjt.get_return()
                    if money <= 0:
                        money = 0
                        df_returns = df_returns.append(
                        {"Hands Played": game_round, "strat": f"Strategy {strat+1}", "dealer": bjt.get_game_state()['player'],
                         'player': bjt.get_game_state()['player'], 'return': stake * bjt.get_return(), 'total': money},
                        ignore_index=True)
                        break
                    # Write the data to the dataframe for later analysis
                    df_returns = df_returns.append(
                        {"Hands Played": game_round, "strat": f"Strategy {strat+1}", "dealer": bjt.get_game_state()['dealer'],
                         'player': bjt.get_game_state()['player'], 'return': stake * bjt.get_return(), 'total': money},
                        ignore_index=True)
                    

                    # Reset BlackJackTable
                    bjt.reset_table()
                df_returns['total'] = df_returns['total'].fillna(0)
                df_loop_sim = df_loop_sim.append(
                        {"strat":df_returns['strat'].iloc[-1], "total hands played": len(df_returns), "ending profit": (df_returns['total'].iloc[-1])-10000,
                         "win %": len(df_returns[df_returns["return"]>0])/len(df_returns),
                         "push %": len(df_returns[df_returns["return"]==0])/len(df_returns),
                         "loss %": len(df_returns[df_returns["return"]<0])/len(df_returns)},
                        ignore_index=True)
            #See how far into the loop I am
            it += 1
            print(it)
            
    df_loop_sim['total hands played'] = df_loop_sim['total hands played'].diff().fillna(df_loop_sim['total hands played']).astype(int)
    


import numpy as np
from collections import namedtuple
from itertools import product
from pprint import pprint
import markov
        
HealthState = namedtuple("HealthState", ['PlayerHealth', 'WildHealth'])

def applyDamage(startState, playerDamage, wildDamage):
    new_player_health = startState.PlayerHealth - playerDamage
    new_wild_health = startState.WildHealth - wildDamage

    if new_player_health<=0 or new_wild_health<=0:
        return 'Failed'
    else:
        return HealthState(new_player_health,new_wild_health)


#Set up MDP instance

player_actions = ['Attack', 'Evade', 'Catch']
catch_probabilities = [None, 0.90, 2/3, 1/3, 0.125]

states = [HealthState(*x) for x in product(range(1,5),range(1,5))] + ['Failed', 'Caught']

wild_action_probabilites = {state:{'Attack':0.40, 'Evade':0.35, 'Run':0.25} for state in states}

#Initialize transition_probabilities dictionary
transition_matrix = {k:np.zeros((len(states),len(states))) for k in player_actions}

for fromState in states:
    if fromState == 'Failed' or fromState=='Caught':
        transition_matrix['Attack'][states.index(fromState)][states.index(fromState)] = 1
        transition_matrix['Evade'][states.index(fromState)][states.index(fromState)] = 1
        transition_matrix['Catch'][states.index(fromState)][states.index(fromState)] = 1
    else:
        #CALCULATE WHEN PLAYER ATTACKS
        transition_matrix['Attack'][states.index(applyDamage(fromState, 1, 1))][states.index(fromState)] += wild_action_probabilites[fromState]['Attack']
        transition_matrix['Attack'][states.index(applyDamage(fromState, 1, 0))][states.index(fromState)] += wild_action_probabilites[fromState]['Evade']
        transition_matrix['Attack'][states.index(applyDamage(fromState, 1, 2))][states.index(fromState)] += wild_action_probabilites[fromState]['Run']
        
        #CALCULATE WHEN PLAYER EVADES
        transition_matrix['Evade'][states.index(applyDamage(fromState, 0, 1))][states.index(fromState)] += wild_action_probabilites[fromState]['Attack']
        transition_matrix['Evade'][states.index(applyDamage(fromState, 0, 0))][states.index(fromState)] += wild_action_probabilites[fromState]['Evade']
        transition_matrix['Evade'][states.index('Failed')][states.index(fromState)] += wild_action_probabilites[fromState]['Run']
        
        #CALCULATE WHEN PLAYER CATCH
        transition_matrix['Catch'][states.index('Caught')][states.index(fromState)] += catch_probabilities[fromState.WildHealth]
        transition_matrix['Catch'][states.index('Failed')][states.index(fromState)] += (1 - catch_probabilities[fromState.WildHealth])
        
rewards = {state:0 for state in states}
rewards['Caught'] = 1
rewards['Failed'] = -1


pokeradar = markov.MDP(states, player_actions, transition_matrix, rewards)
pokeradar.value_iteration()
pokeradar.report_policy()

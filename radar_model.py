import numpy as np
from collections import namedtuple
from itertools import product
from pprint import pprint
import markov

#Initalize state structures
RadarState = namedtuple("RadarState", ['PlayerHealth', 'WildHealth', 'PreviousTurnOutcome'])
possibleOutcomes = {'start', 'wildattack', 'crit', 'wildevade', 'staredown'}


def applyDamage(startState, playerDamage, wildDamage, turnOutcome):
    '''Applies damage and returns the new state'''
    new_player_health = startState.PlayerHealth - playerDamage
    new_wild_health = startState.WildHealth - wildDamage

    if new_player_health<=0 or new_wild_health<=0:
        return 'Failed'
    else:
        return RadarState(new_player_health, new_wild_health, turnOutcome)

player_actions = ['Attack', 'Evade', 'Catch']
catch_probabilities = [None, 0.97, 0.79, 0.66, 0.56]

states = [RadarState(*x) for x in product(range(1,5),range(1,5), possibleOutcomes)] + ['Failed', 'Caught']

wild_action_probabilities = {
    'start':            {'Attack':0.45, 'Evade':0.35, 'Run':0.20}, #index 0
    'wildattack':       {'Attack':0.40, 'Evade':0.30, 'Run':0.30}, #index 1
    'crit':             {'Attack':0.50, 'Evade':0.40, 'Run':0.10}, #index 2
    'wildevade':        {'Attack':0.60, 'Evade':0.30, 'Run':0.10}, #index 3
    'staredown':        {'Attack':0.20, 'Evade':0.30, 'Run':0.50}  #index 4
}

#Initialize transition_probabilities dictionary
#The matrix will be indexed as such transition_matrix[toStateIndex][fromStateIndex]
transition_matrix = {k: np.zeros((len(states),len(states))) for k in player_actions}

for fromState in states:
    i_fromState = states.index(fromState)
    if fromState == 'Failed' or fromState=='Caught':
        transition_matrix['Attack'][i_fromState][i_fromState] = 1
        transition_matrix['Evade'][i_fromState][i_fromState] = 1
        transition_matrix['Catch'][i_fromState][i_fromState] = 1
    else:
        #Calculate when Player Attacks and Wild Attacks
        i_toState = states.index(applyDamage(fromState, 1, 1, 'wildattack'))
        transition_probability = wild_action_probabilities[fromState.PreviousTurnOutcome]['Attack']
        transition_matrix['Attack'][i_toState][i_fromState] += transition_probability

        # Calculate when Player Attacks and Wild Evades
        i_toState = states.index(applyDamage(fromState, 1, 0, 'wildevade'))
        transition_probability = wild_action_probabilities[fromState.PreviousTurnOutcome]['Evade']
        transition_matrix['Attack'][i_toState][i_fromState] += transition_probability

        # Calculate when Player Attacks and Wild Runs
        i_toState = states.index(applyDamage(fromState, 1, 2,'crit'))
        transition_probability = wild_action_probabilities[fromState.PreviousTurnOutcome]['Run']
        transition_matrix['Attack'][i_toState][i_fromState] += transition_probability
        
        # Calculate when Player Evades and Wild Attacks
        i_toState = states.index(applyDamage(fromState, 0, 1, 'wildattack'))
        transition_probability = wild_action_probabilities[fromState.PreviousTurnOutcome]['Attack']
        transition_matrix['Evade'][i_toState][i_fromState] += transition_probability

        # Calculate when Player Evades and Wild Evades
        i_toState = states.index(applyDamage(fromState, 0, 0,'staredown'))
        transition_probability = wild_action_probabilities[fromState.PreviousTurnOutcome]['Evade']
        transition_matrix['Evade'][i_toState][i_fromState] += transition_probability

        # Calculate when Player Evades and Wild Runs
        i_toState = states.index('Failed')
        transition_probability = wild_action_probabilities[fromState.PreviousTurnOutcome]['Run']
        transition_matrix['Evade'][i_toState][i_fromState] += transition_probability
        
        # Calculate when Player Catches (success)
        i_toState = states.index('Caught')
        transition_probability = catch_probabilities[fromState.WildHealth]
        transition_matrix['Catch'][i_toState][i_fromState] += transition_probability

        # Calculate when Player Catches (fail)
        i_toState = states.index('Failed')
        transition_probability = (1 - catch_probabilities[fromState.WildHealth])
        transition_matrix['Catch'][i_toState][i_fromState] += transition_probability
        
rewards = {state: 0 for state in states}
rewards['Caught'] = 1
rewards['Failed'] = -1

pokeradar = markov.MDP(states, player_actions, transition_matrix, rewards)
pokeradar.value_iteration()
pokeradar.report_policy()

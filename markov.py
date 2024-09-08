import numpy as np

class Chain:
    def __init__(self, states, transitions, current_state=None):
        self.states = states
        self.transitions = transitions
        if current_state is None:
            self.current_state = np.array([1 if i == 0 else 0 for i in range(len(states))])
        else:
            self.current_state = current_state

    def advance_state(self):
        '''Advacnes the state vector by one step acording the the transition matrix'''
        self.current_state = np.array(self.transitions @ self.current_state)

    def advance_n_states(self, n):
        '''Advacnes the state vector by n steps acording the the transition matrix'''
        for _ in range(n):
            self.advance_state()

    def steady_state(self):
        '''Finds the steady-state state vector'''
        # Gets the eigenvalues and eigenvectors of the matrix
        eigenvalues, eigenvectors = np.linalg.eig(self.transitions)

        # We transpose the output from numpty so that we can easily index it
        eigenvectors = np.transpose(eigenvectors)

        # Gets candidates for steady-state vecotrs by finding vectors with eigenvalue=1
        # There should only be one candidate
        steady_state_vectors = [v for (lam, v) in zip(eigenvalues, eigenvectors) if np.isclose(lam, 1)]

        # If such a vector exists, normalize it and return it
        if steady_state_vectors:
            ss_vector = steady_state_vectors[0].real
            ss_vector = ss_vector / sum(ss_vector)
            if np.all(ss_vector >= 0):  # Check for non-negative probabilities
                return ss_vector
            else:
                raise ValueError("Steady state vector contains negative probabilities.")

        # If no vector was foumd, return nothing
        return None


class MDP(Chain):  # Inherits from your Chain class
    def __init__(self, states, actions, transitions, rewards, current_state=None, gamma=0.9):
        super().__init__(states, transitions, current_state)
        self.actions = actions
        self.rewards = rewards
        self.values = np.zeros(len(states))
        self.gamma = gamma  # Gamma represents the discount factor for rewards
        self.policy = {state: None for state in states}

    def advance_state_with_action(self, action):
        self.current_state = np.array(self.transitions[action] @ self.current_state)

    def single_value_iteration(self):
        '''Iterate a single time on the value function
        The value function represents the expected value of being in a state and choosing the best action
        It is initilized at 0 for all states, and we use dynamic programming to converge on the correct values
        This implements the Bellman equation for the MDP
        '''
        for fromState in self.states:
            # For each state and action get the sum of possible rewards across all state transitions
            values_for_actions = [sum(
                [self.transitions[action][self.states.index(toState)][self.states.index(fromState)]
                 * (self.rewards[toState] + self.gamma * self.values[self.states.index(toState)])
                 for toState in self.states])
                for action in self.actions]

            # Based on the above calculation, find the max value from the best action
            best_action_index = np.argmax(values_for_actions)
            self.policy[fromState] = self.actions[best_action_index]
            self.values[self.states.index(fromState)] = values_for_actions[best_action_index]

    def value_iteration_n(self, n):
        for _ in range(n):
            self.value_iteration()

    def value_iteration(self, theta=0.0001, max_n=100):
        '''Converges on the value function with tolerance theta.'''
        n = 0
        while True:
            initial_values = np.copy(self.values)
            self.single_value_iteration()
            deltas = np.absolute(initial_values - self.values)
            delta = max(deltas)
            n += 1
            if delta < theta or n >= max_n:
                return n

    def report_policy(self):
        '''Prints the current policy'''
        for state in self.states:
            print(f"{state}\t{self.policy[state]}\t{self.values[self.states.index(state)]}")
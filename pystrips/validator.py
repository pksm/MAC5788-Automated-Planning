# validator.py
# -----------------------------------------------------------------------
# Paula Kintschev S. de Moraes
# Numero USP: 10380758
# ------------------------------------------------------------------------

import util
from state import State

def applicable(state,a):
    return State(state).intersect(a.precond) == a.precond

def successor(state, action):
    return State(action.pos_effect).union(State(state).difference(action.neg_effect))

def goal_test(problem, state):
    return State(state).intersect(problem) == State(problem)

def validate(problem, solution):
    state = problem.init
    goal = problem.goal
    for a in solution:
        if not applicable(state,a): # Check if an action is applicable in a given current state
            return False
        currentProp = state 
        state = successor(state,a)
        if state.intersect(a.pos_effect) != a.pos_effect: # Check if an action positive effects was replicated to a successor state
            return False
        notAffected = currentProp.difference(a.neg_effect)
        if state.intersect(notAffected) != notAffected: # Check if an atom that was not supposed to change was deleted by an action
            return False 
        if state.intersect(a.neg_effect) != State([]): # Check if no negative effects was replicated to a successor state
            return False
    return goal_test(goal,state) # Check if after running all actions in a given solution we get to the problem's goal

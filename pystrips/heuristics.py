# heuristics.py
# -----------------------------------------------------------------------
# Paula Kintschev S. de Moraes
# Numero USP: 10380758
# ------------------------------------------------------------------------

import util
from state import State
from node import Node
import sys

def applicable(state, actions):
    ''' Return a list of applicable actions in a given `state`. '''
    app = list()
    for act in actions:
        if State(state).intersect(act.precond) == act.precond:
            app.append(act)
    return app

def successorRelaxed(state, action):
    ''' Return the sucessor state generated by executing `action` in `state`. '''
    return State(action.pos_effect).union(state)

def layerGoals(state, predicates):
    return State(state).union(predicates)

def goal_test(state, goal):
    ''' Return true if `state` is a goal state. '''
    return State(state).intersect(goal) == State(goal)

def h_naive(state, planning):
    return 0
    
def h_add(state, planning):
    h = dict() 
    actions = planning._all_actions
    goal = planning._problem.goal
    X = state
    for x in X:
        h[x] = 0
    change = True
    while change:
        change = False
        actionsApplicable = applicable(X,actions)
        for a in actionsApplicable:
            X = successorRelaxed(X,a) #added positive effects of a
            for p in a.pos_effect:
                prev = h.get(p,sys.maxsize)

                #h[p] = min(prev,(1+sum([h.get(pre, sys.maxsize) for pre in a.precond  ])))
                h[p] = min(prev,(1+sum(h.get(pre, sys.maxsize) for pre in a.precond)))
                if prev != h[p]:
                    change = True
    return sum(h.get(i,sys.maxsize) for i in goal)
    
def h_max(state, planning):
    h = dict() 
    actions = planning._all_actions
    goal = planning._problem.goal
    X = state
    for x in X:
        h[x] = 0
    change = True
    while change:
        change = False
        actionsApplicable = applicable(X,actions)
        for a in actionsApplicable:
            X = successorRelaxed(X,a) #added positive effects of a
            for p in a.pos_effect:
                prev = h.get(p,float('inf'))
                h[p] = min(prev,(1+max(h.get(pre, float('inf')) for pre in a.precond)))
                if prev != h[p]:
                    change = True
    return max(h.get(i,float('inf')) for i in goal)

def firstLevel(atom, graph):
    for level, _ in graph.keys():
        if atom in graph[level,'fact']:
            return level

def h_ff(state, planning):
    graphplan = dict() #graphplan relaxed
    actions = planning._all_actions
    goal = planning._problem.goal
    X = state
    isGoal = False
    if X.intersect(goal) == goal: #ja estamos na meta entao o compimento (a quantidade) de acoes necessaria eh zero
        return 0
    level = 0
    graphplan[(level,'fact')] = X
    #PHASE 1 - expand graph
    while not isGoal:
        actionsApplicable = applicable(X,actions)
        level += 1
        for a in actionsApplicable:
            X = successorRelaxed(X,a) #added positive effects of a
            if X.intersect(goal) == goal:
                isGoal = True
                break
        graphplan[(level,'fact')] = X
        graphplan[(level,'action')] = actionsApplicable

    #PHASE 2 - extracting a relaxed plan
    count_actions = 0
    levelGoals = dict() # dict of states or empty sets
    for t in range(level+1):    
        levelGoals[t] = graphplan[(t,'fact')].intersect(goal)
    # here t has the same value of level
    while(t >= 1):
        for g in levelGoals[t]:
            for a in graphplan[(t,'action')]:
                if (g in a.pos_effect):
                    count_actions += 1
                    break
            for p in a.precond:
                fLevel = firstLevel(p, graphplan)
                levelGoals[fLevel] = levelGoals[fLevel].union(State(p))      
        t -= 1 

    return count_actions

# planner.py
# -----------------------------------------------------------------------
# Paula Kintschev S. de Moraes
# Numero USP: 10380758
# ------------------------------------------------------------------------

from util import Queue, PriorityQueue, Stack
from state import State
from node  import Node


# class Frontier(object):
#     '''
#     Frontier class implement a search frontier using a
#     PriorityQueue for ordering the nodes and a set for
#     constant-time checks of states in frontier.

#     OBSERVATION: it receives as input a function `f` that
#     itself receives a node and returns the priority for
#     the given node. Check util.PriorityQueueWithFunction for
#     more details.
#     '''

#     def __init__(self, f):
#         self._queue = util.PriorityQueue()
#         self._set = set()

#     def __contains__(self, node):
#         ''' Return true if `node.state` is in the frontier. '''
#         return node.state in self._set

#     def __len__(self):
#         ''' Return the number of nodes in frontier. '''
#         assert(len(self._queue) == len(self._set))
#         return len(self._queue)

#     def is_empty(self):
#         ''' Return true if frontier is empty. '''
#         return self._queue.isEmpty()

#     def push(self, node):
#         ''' Push `node` to frontier. '''
#         self._queue.push(node)
#         self._set.add(node.state)

#     def pop(self):
#         ''' Pop `node` from frontier. '''
#         node = self._queue.pop()
#         self._set.remove(node.state)
#         return node

#     def __str__(self):
#         ''' Return string representation of frontier. '''
#         return str(self._queue)


class ProgressionPlanning(object):
    '''
    ProgressionPlanning class implements all necessary components
    for implicitly generating the state space in a forward way (i.e., by progression).self
    '''

    def __init__(self, domain, problem):
        self._problem = problem
        self._all_actions = problem.ground_all_actions(domain)

    @property
    def problem(self):
        return self._problem

    @property
    def actions(self):
        return self._all_actions

    def applicable(self, state):
        app = list()
        for act in self.actions:
            if State(state).intersect(act.precond) == act.precond:
                app.append(act)
        return app

    def successor(self, state, action):
        return State(action.pos_effect).union(State(state).difference(action.neg_effect))

    def goal_test(self, state):
        return State(state).intersect(self.problem.goal) == State(self.problem.goal)

    def solve(self,heuristic):
        plan = []
        num_explored = 0
        num_generated = 0
        opened = set()
        initialNode = Node(State(self.problem.init))
        frontier = PriorityQueue()
        frontier.update(initialNode, initialNode.g)
        goal = False
        while not goal:
            sNode = frontier.pop()
            opened.add(sNode.state)
            num_explored += 1
            if self.goal_test(sNode.state):
                goal = True
                break
            actionsApplicable = self.applicable(sNode.state)
            for action in actionsApplicable:
                stateSon = self.successor(sNode.state, action)
                if stateSon in opened:
                    continue
                num_generated += 1
                nodeSon = Node(stateSon,
                               action,
                               sNode,
                               sNode.g + 1,
                               heuristic(stateSon, self))
                fSon = nodeSon.g + nodeSon.h
                if nodeSon not in frontier:
                    frontier.push(nodeSon, fSon)
                else:
                    incumbent = frontier[nodeSon]
                    if fSon < (incumbent.h + incumbent.g):
                        frontier.update(nodeSon, fSon)
            if frontier.isEmpty():
                print ('Problem does not have a solution')
                return None
        plan = sNode.path()
        return (plan, num_explored, num_generated)

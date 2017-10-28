from util import Queue, PriorityQueue, Stack
from state import State
from node import Node
from grounding import Grounding


class ProgressionPlanning(object):
    '''
    ProgressionPlanning class implements all necessary components
    for implicitly generating the state space
    in a forward way (i.e., by progression).self
    '''

    def __init__(self, domain, problem):
        self._domain = domain
        self._problem = problem
        if domain is not None and problem is not None:
            self.grounding = Grounding(self._domain, self._problem)

    @property
    def domain(self):
        return self._domain

    @property
    def problem(self):
        return self._problem

    def solve(self, typeSearch, heuristic):
        """
        Function that solves the plannng problem.

        :type typeSearch: int
        :type heuristic: str
        :rtype: (list of str, int, int)
        """
        if (typeSearch == 0):  # Depth First Search
            return self.dfs()
        elif (typeSearch == 1):
            return self.bfs()  # Breadth First Search
        elif (typeSearch == 2):
            return self.astar(heuristic)  # A-Star Search

    def getInit(self):
        return self.problem.init  # return a set with the initial propositions

    def isGoal(self, state):
        return ((self.problem.goal & set(state)) == self.problem.goal)

    def successor(self, state, action):
        positive_act = State(set(action.pos_effect))
        remove_neg_from_state = state.difference(State(set(action.neg_effect)))
        return State(positive_act).union(remove_neg_from_state)

    def astar(self, heuristic):
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
            if self.isGoal(sNode.state):
                goal = True
                break
            actionsApplicable = self.grounding.applicableActions(sNode.state)
            for action in actionsApplicable:
                stateSon = self.successor(sNode.state, action)
                if stateSon in opened:
                    continue
                num_generated += 1
                nodeSon = Node(stateSon,
                               action,
                               sNode,
                               sNode.g + 1,
                               heuristic(stateSon,
                                         self.problem,
                                         self.grounding))
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

    def bfs(self):
        plan = []
        num_explored = 0
        num_generated = 0
        opened = set()
        naBorda = set()
        initialNode = Node(State(self.getInit()))
        nodesNext = Queue()
        nodesNext.push(initialNode)
        naBorda.add(initialNode.state)
        goal = False
        while not goal:
            sNode = nodesNext.pop()
            naBorda.remove(sNode.state)
            opened.add(sNode.state)
            num_explored += 1
            actionsApplicable = self.grounding.applicableActions(sNode.state)
            for a in actionsApplicable:
                stateSon = self.successor(sNode.state, a)
                num_generated += 1
                if stateSon in opened or stateSon in naBorda:
                    continue
                nodeSon = Node(stateSon, a, sNode, sNode.g + 1)
                if self.isGoal(stateSon):
                    goal = True
                    sNode = nodeSon
                    break
                nodesNext.push(nodeSon)
                naBorda.add(stateSon)
            if nodesNext.isEmpty():
                print ('Problem does not have a solution')
                return None
        plan = sNode.path()
        return (plan, num_explored, num_generated)

    def dfs(self):
        plan = []
        num_explored = 0
        num_generated = 0
        opened = set()
        initialNode = Node(State(self.getInit()))
        nodesNext = Stack()
        nodesNext.push(initialNode)
        goal = False
        while not goal:
            sNode = nodesNext.pop()
            opened.add(sNode.state)
            num_explored += 1
            if self.isGoal(sNode.state):
                goal = True
                break
            actionsApplicable = self.grounding.applicableActions(sNode.state)
            for action in actionsApplicable:
                stateSon = self.successor(sNode.state, action)
                num_generated += 1
                if stateSon in opened:
                    continue
                nodeSon = Node(stateSon, action, sNode, sNode.g + 1)
                nodesNext.push(nodeSon)
            if nodesNext.isEmpty():
                print ('Problem does not have a solution')
                return None
        plan = sNode.path()
        print(plan)
        return (plan, num_explored, num_generated)

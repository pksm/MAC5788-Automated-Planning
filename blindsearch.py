'''
*********DEPRECATED*************** use planner.py insteaded

First attempt to create a class for Automated Planning

Options:
- a class that grounds all predicates at once and returns a set of instantiated actions
- a class called by blindSearch that given a domain and a set of atoms returns a list of valid grounded actions
*- only one class that ground actions and implements the search 

Criar arquivo de teste, exemplos de teste:
- teste da função getInit com uma comparação com o que foi imputado no pddl
- teste da função isGoal com a meta do problema e uma entrada manual da entrada da meta
'''
import re
from copy import deepcopy
from itertools import product

from util import Stack, Queue
from state import State
from node  import Node
from action import Action, GroundedAction


def generate(typ,lit): #lit eh um dict (literals) --- retorna todas as subst possiveis para uma acao
	combList = []
	if (len(typ)==1):
		return lit[typ[0]]  
	for t in typ:
		combList.append(lit[t])
	allComb = list(product(*combList))
	return allComb

def subst(comb,act): 
	pos = 0
	instAct = deepcopy(act)
	pos_effect = set()
	neg_effect = set()
	for valor in comb:
		act._params[pos]._value = valor
		instAct._params[pos]._value = valor
		pos += 1
	for pre in range(len(act._precond)):
		instAct._precond[pre]._predicate = act._precond[pre]._predicate.ground(act._params)
		if ((instAct.precond[pre].predicate.name == '=') and (str(instAct.precond[pre].predicate.args[0]) == str(instAct.precond[pre].predicate.args[1]))):
			return None
	for eff in range(len(act._effects)):
		instAct._effects[eff]._predicate = act._effects[eff]._predicate.ground(act._params)
		if act._effects[eff].is_positive():
			pos_effect.add(str(instAct._effects[eff]._predicate))
		else:
			neg_effect.add(str(instAct._effects[eff]._predicate))
	# for eff in instAct.effects:
	# 	if eff.is_positive():
	# 		pos_effect.add(str(eff.predicate))
	# 	elif eff.is_negative():
	# 		#instAct._neg_effect.add(str(eff.predicate))
	# 		neg_effect.add(str(eff.predicate))
	args = [ str(param.value) for param in instAct.params ]
	precond = [ str(l.predicate) for l in instAct._precond if l.is_positive() ]

	return GroundedAction(instAct.name, args, precond, pos_effect, neg_effect)

# def applicable(state, actions):
# 	app = list()
# 	for act in actions:
# 		precond = act.precond
# 		if state.intersect(set(precond)) == set(precond):
# 			app.append(act)
# 	return app


class blindSearch(object):
	"""docstring for blindSearch"""
	def __init__(self, domain, problem, search=None):
		#super(blindSearch, self).__init__()
		self._domain = domain
		self._problem = problem
		self._search = search
		self.operatorsPrecond = {}
		self.all_actions = self.domain.operators
		self.literals = self.problem.objects #dict key -> type   values -> literals
		self.genDict()
		#self._objects[obj.type] = self._objects.get(obj.type, [])
		# self.domainOperators = {}
		# for i in self.domain.operators:
		# 	self.domainOperators[i.name] = []
		# 	for j in i.precond:
		# 		self.domainOperators[i.name].append(str(j))

	@property
	def domain(self):
		return self._domain

	@property
	def problem(self):
		return self._problem

	@property
	def search(self):
		return self._search

	def genDict(self):
		for a in self.all_actions:
			for p in a.precond:
				if p.predicate.name != '=':
					self.operatorsPrecond[a] = self.operatorsPrecond.get(a, set()) #na hora de fazer union, intersect, difference mudar para set
					self.operatorsPrecond[a].add(re.sub(r'\([^)]*\)', '', str(p)))

	def getInit(self):
		return self.problem.init #return a set with the initial propositions

	def isGoal(self, state):
		return ((self.problem.goal & set(state)) == self.problem.goal) 

	def grounding(self, actions): #returns list of instatiated applicable actions
		actToGround = []
		for a in actions:
			typ = [i.type for i in a.params]
			combAll = generate(typ, self.literals)
			for i in combAll:
				ac = subst(list(i), a) 
				if ac is not None:
					actToGround.append(ac)
		return actToGround

	def applicableActions(self,state): #esperando um state do tipo set
		validActions = set()
		app = list()
		atomState = {re.sub(r'\([^)]*\)', '', str(i)) for i in state} 
		for i in self.operatorsPrecond.keys():
			if ((self.operatorsPrecond[i] & atomState) == self.operatorsPrecond[i]):
				validActions.add(i)
		instatiatedActions = self.grounding(validActions)
		for act in instatiatedActions:
			precond = act.precond
			if state.intersect(set(precond)) == set(precond):
				app.append(act)
		return app
    
	def successor(self, state, action):
		return State(State(set(action.pos_effect))).union(state.difference(State(set(action.neg_effect))))

	def solveBreadth(self):
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
			while not goal :
				sNode = nodesNext.pop()
				naBorda.remove(sNode.state)
				opened.add(sNode.state)
				num_explored += 1
				actionsApplicable = self.applicableActions(sNode.state)
				for a in actionsApplicable:					
					stateSon = self.successor(sNode.state,a)
					num_generated += 1
					if stateSon in opened or stateSon in naBorda:
						continue 
					nodeSon = Node(stateSon,a,sNode,sNode.g + 1)
					if self.isGoal(stateSon):
						goal = True
						sNode = nodeSon
						break
					nodesNext.push(nodeSon)
					naBorda.add(stateSon)
				if nodesNext.isEmpty():
					print ('Problem does not have a solution')
					return None
			plan= sNode.path()
			#print(plan)
			return (plan,num_explored,num_generated)

	def solveDepth(self):
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
			while not goal :
				sNode = nodesNext.pop()
				naBorda.remove(sNode.state)
				opened.add(sNode.state)
				num_explored += 1
				actionsPossible = self.applicableActions(set(sNode.state))
				actionsApplicable = applicable(sNode.state, actionsPossible)
				#realOnes = applicable(sNode.state, actionsApplicable)
				for a in actionsApplicable:					
					stateSon = self.successor(sNode.state,a)
					num_generated += 1
					if stateSon in opened or stateSon in naBorda:
						continue 
					nodeSon = Node(stateSon,a,sNode,sNode.g + 1)
					if self.isGoal(stateSon):
						goal = True
						sNode = nodeSon
						break
					nodesNext.push(nodeSon)
					naBorda.add(stateSon)
				if nodesNext.isEmpty():
					print ('Problem does not have a solution')
					return None
			plan= sNode.path()
			#print(plan)
			return (plan,num_explored,num_generated)
		 


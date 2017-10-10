import re
from copy import deepcopy
from itertools import product
from action import GroundedAction

class Grounding(object):
    def __init__(self, domain, problem):
        self._domain = domain
        self._problem = problem
        self.operatorsPrecond = {}
        self.all_operators = self.domain.operators
        self.literals = self.problem.objects 
        self.genDict()
    
    @property
    def domain(self):
        return self._domain

    @property
    def problem(self):
        return self._problem

    def genDict(self):
            for a in self.all_operators:
                for p in a.precond:
                    if p.predicate.name != '=':
                        self.operatorsPrecond[a] = self.operatorsPrecond.get(a, set()) #na hora de fazer union, intersect, difference mudar para set
                        self.operatorsPrecond[a].add(re.sub(r'\([^)]*\)', '', str(p)))

    def generate(self,typ,lit): 
        combList = []
        if (len(typ)==1):
            return lit[typ[0]]  
        for t in typ:
            combList.append(lit[t])
        allComb = list(product(*combList))
        return allComb

    def subst(self,comb,act): ###########
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
        args = [ str(param.value) for param in instAct.params ]
        precond = [ str(l.predicate) for l in instAct._precond if l.is_positive() ]

        return GroundedAction(instAct.name, args, precond, pos_effect, neg_effect)

    def ground(self, actions): 
        actToGround = []
        for a in actions:
            typ = [i.type for i in a.params]
            combAll = self.generate(typ, self.literals)
            for i in combAll:
                ac = self.subst(list(i), a) 
                if ac is not None:
                    actToGround.append(ac)
        return actToGround

    def applicableActions(self,state): #returns list of instatiated applicable actions
        validActions = set()
        app = list()
        atomState = {re.sub(r'\([^)]*\)', '', str(i)) for i in state} 
        for i in self.operatorsPrecond.keys():
            if ((self.operatorsPrecond[i] & atomState) == self.operatorsPrecond[i]):
                validActions.add(i)
        instatiatedActions = self.ground(validActions)
        #print ("Actions", instatiatedActions[0], "Name: ", instatiatedActions[0].name, "Params: ", instatiatedActions[0].params, type(instatiatedActions[0].params), "Precond: ", instatiatedActions[0].precond, "Pos eff> ", instatiatedActions[0].pos_effect)
        for act in instatiatedActions:
            precond = act.precond
            if state.intersect(set(precond)) == set(precond):
                app.append(act)
        return app

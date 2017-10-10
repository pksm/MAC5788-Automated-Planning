import unittest
from planner import ProgressionPlanning
from action import GroundedAction
from state import State

class TestSuccessor(unittest.TestCase):

 	def setUp(self):
 		self.action = GroundedAction('sample_soil', \
 			['rover0', 'rover0store', 'waypoint2'], \
 			['at(rover0, waypoint2)', 'at_soil_sample(waypoint2)', 'equipped_for_soil_analysis(rover0)', 'store_of(rover0store, rover0)', 'empty(rover0store)'], \
 			{'full(rover0store)', 'have_soil_analysis(rover0, waypoint2)'}, \
 			{'at_soil_sample(waypoint2)', 'empty(rover0store)'}) 
 		self.state = State({'visible(waypoint1, waypoint2)','at(rover0, waypoint2)', 'at_soil_sample(waypoint2)', 'available(rover0)','equipped_for_soil_analysis(rover0)', 'store_of(rover0store, rover0)', 'empty(rover0store)'})
 		self.expectedResult = State({'visible(waypoint1, waypoint2)','at(rover0, waypoint2)', 'available(rover0)','equipped_for_soil_analysis(rover0)', 'store_of(rover0store, rover0)', 'full(rover0store)', 'have_soil_analysis(rover0, waypoint2)'})
 		self.plan = ProgressionPlanning(None,None)

 	def test_successor(self):
 		successor = self.plan.successor(self.state, self.action)
 		self.assertEqual(successor, self.expectedResult)

 	def test_posEffect_in_successor(self):
 		successor = self.plan.successor(self.state, self.action)
 		self.assertTrue(self.action.pos_effect.issubset(set(successor)))

 	def test_negEffect_not_in_successor(self):
 		successor = self.plan.successor(self.state, self.action)
 		self.assertTrue(self.action.neg_effect.isdisjoint(set(successor)))

if __name__ == '__main__':
    unittest.main()
from abc import abstractmethod
import math


class Heuristic():
    """ Base class for a heuristic"""

    @abstractmethod
    def value_for(self, tree_node):
        """ Return the heuristic value for 'tree_node' """
        pass
    
class Manhattan():
    def __init__(self, goal_state):
        self.goal_state = goal_state

    def value_for(self, tree_node):
       return abs(self.goal_state.get_X() - tree_node.state.get_X()) + abs(self.goal_state.get_Y() - tree_node.state.get_Y())

    
class Euclidian():
    def __init__(self, goal_state):
        self.goal_state = goal_state

    def value_for(self, tree_node):
        return math.sqrt((self.goal_state.get_X() - tree_node.state.get_X())**2 + 
                                            (self.goal_state.get_Y() - tree_node.state.get_Y())**2)
    

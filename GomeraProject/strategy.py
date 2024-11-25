from abc import abstractmethod

class SearchStrategy(): 
    """ Base class for a search strategy """

    @abstractmethod
    def frontier_value(self, tree_node):
        """ The frontier value that search node has under this strategy. It may modify some attributes
        for the search node """
        pass
    
class BFS():
    def frontier_value(self, tree_node):
        return tree_node.depth
    
class DFS(): 
    def frontier_value(self, tree_node):
        return 1 / (tree_node.depth + 1)
    
class UCS(): 
    def frontier_value(self, tree_node):
        return tree_node.distance_cost
    
class Greedy():
    def __init__(self, heuristic):
        self.heuristic = heuristic

    def frontier_value(self, tree_node):
        tree_node.heuristic = self.heuristic.value_for(tree_node)
        return tree_node.heuristic

class AStar():
    def __init__(self, heuristic):
        self.heuristic = heuristic

    def frontier_value(self, tree_node):
        tree_node.heuristic = self.heuristic.value_for(tree_node)
        return tree_node.distance_cost + tree_node.heuristic


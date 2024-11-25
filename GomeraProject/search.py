from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
from prioirity_queue import PriorityQueue

if TYPE_CHECKING:
    from strategy import SearchStrategy


@dataclass
class Transition:
    """Class which stores the state transition of the successors"""
    action: str
    state: State 
    distance:float
    slope: float

    def __str__(self):
        return f"({self.action},{self.state.get_id()},({self.distance},{self.slope})"

class State:
    def __init__(self, Y, X, island_map):
        self.island_map = island_map
        self.X = X
        self.Y = Y
    
    def get_X(self): 
        return self.X
    
    def get_Y(self): 
        return self.Y
 
    def get_id(self):
        return f"({self.Y},{self.X})"
    
    def successors(self, factor_size, max_slope):
        """Calculate the successors"""

        directions = ['N', 'E', 'S', 'W']
        successors = []
        direction_changes = {
        'N': (0, 1),
        'E': (1, 0),
        'S': (0, -1),
        'W': (-1, 0)
        }
        for direction in directions:
            change_X, change_Y = direction_changes.get(direction, (0, 0))

            succ_X = self.X + self.island_map.size_cell * factor_size * change_X
            succ_Y = self.Y + self.island_map.size_cell * factor_size * change_Y

            succesor_state = State(succ_Y,succ_X, self.island_map)
            slope = abs(
                self.island_map.umt_YX(self.Y, self.X) - self.island_map.umt_YX(succ_Y, succ_X)
            ) 
            if (self.island_map.umt_YX(self.Y, self.X) != self.island_map.nodata_value and 
                self.island_map.umt_YX(succ_Y, succ_X) != self.island_map.nodata_value and 
                slope < max_slope
            ):
                transition = Transition(direction, succesor_state ,self.island_map.size_cell * factor_size, slope)
                successors.append(transition)
        return successors

    
class Problem:
    def __init__(self, island_map, initial, goal):
        self.island_map = island_map
        self.initial = State(initial[0], initial[1], island_map)
        self.goal = State(goal[0], goal[0], island_map)

    def goal_test(self, current):
        return current.X == self.goal.X and current.Y == self.goal.Y

class TreeNode:
    def __init__(self, state, id, strategy, distance_cost=0, maximum_slope_cost=0,
                 depth=0, parent=None, action=None, frontier_value=None, heuristic=None):
        self.state = state
        self.id = id
        self.strategy = strategy
        self.distance_cost = distance_cost
        self.maximum_slope_cost = maximum_slope_cost
        self.depth = depth
        self.parent = parent
        self.action = action
        self.frontier_value = frontier_value
        self.heuristic = heuristic

        self.frontier_value = self.strategy.frontier_value(self)

    def create_child(self, id, transition):
        new_distance_cost = self.distance_cost + transition.distance
        new_maximum_slope = max(self.maximum_slope_cost, transition.slope)

        return TreeNode(
            state=transition.state,
            id=id,
            strategy=self.strategy,
            distance_cost=new_distance_cost,
            maximum_slope_cost=new_maximum_slope,
            depth=self.depth + 1,
            parent=self,
            action=transition.action
        )

    def solution_path_from_root(self):
        solution = []
        while self is not None:
            solution.insert(0, self)
            self = self.parent
        return solution

    @classmethod
    def as_root(cls, state, strategy):
        return cls(state, 0, strategy)

    def __str__(self):
        id_parent = self.parent.id if self.parent else None
        heuristic = f"{self.heuristic:.3f}" if self.heuristic is not None else 0.0

        return (
            f"[{self.id}][({self.distance_cost:.3f},{self.maximum_slope_cost:.3f}),"
            f"{self.state.get_id()},{id_parent},{self.action},{self.depth},{heuristic},{self.frontier_value:.4f}]"
        )

def search_algorithm(problem, strategy, factor_size, max_slope, max_depth):
    visited = {}
    frontier = PriorityQueue((
        lambda item: item.frontier_value,
        lambda item: item.id
    ))

    frontier.insert(TreeNode.as_root(problem.initial, strategy)) # Insert inital node in frontier 
    tree_node_id = 1
    while not frontier.is_empty():
        tree_node = frontier.remove()
        state_id  = tree_node.state.get_id()
    
        if problem.goal_test(tree_node.state):
            return tree_node
        
        if tree_node.depth == max_depth:
            continue

        # Checked if the id is already in the visited dictionary 
        if state_id in visited and visited[state_id]:
            continue

        # Add to the dictionary the visited id
        visited[state_id] = True

        for transition in tree_node.state.successors(factor_size, max_slope):
            frontier.insert(tree_node.create_child(tree_node_id, transition))
            tree_node_id += 1

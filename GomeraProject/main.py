from __future__ import annotations
from map_island import Map, mean_func, max_func, min_func
from search import Problem, State
import search
from strategy import DFS, BFS, UCS, AStar, Greedy
from heuristic import Euclidian, Manhattan



def choose_strategy(choice: int, goal_state: State):
    if choice == 1: 
        return  DFS()
    elif choice == 2:
        return BFS()
    elif choice == 3: 
        return UCS()
    elif choice == 4: 
        return AStar(Euclidian(goal_state))
    elif choice == 5: 
        return AStar(Manhattan(goal_state))
    elif choice == 6:
        return Greedy(Euclidian(goal_state))
    elif choice == 7: 
        return Greedy(Manhattan(goal_state))
    else: 
        raise ValueError(f"This is not a valid strategy")
    
def show_menu():
    print() 
    print("Choose an option:")
    print("1. DFS")
    print("2. BFS")
    print("3. UCS")
    print("4. A* with Euclidean heuristic")
    print("5. A* with Manhattan heuristic")
    print("6. Greedy with Euclidean heuristic")
    print("7. Greedy with Manhattan heuristic")
    print("8. Exit")
    print()


def show_path(goal_tree_node):
    path_solution = goal_tree_node.solution_path_from_root()
    for tree_node in path_solution:
        print(tree_node)

if __name__ == "__main__":
    original_island_map = Map("LaGomera.hdf5")
    resized_island_map = original_island_map.resize(300, mean_func, "Zoom300Gomera")
    inital_coords = (3105001, 279133)
    goal_coords = (3119401, 280333)
    problem = Problem(resized_island_map, inital_coords, goal_coords)
    goal_state = State(goal_coords[0], goal_coords[1], resized_island_map)
    maximum_slope = 100
    maximum_depth = 500000

    while True:
        print(f"Initial coordinates (Y,X): {inital_coords}")
        print(f"Final coordinates (Y,X): {goal_coords}")
        print(f"Maximum slope (Y,X): {maximum_slope}")
        print(f"Maximum depth level: {maximum_depth} ")
        show_menu()
        choice = (input("Enter your choice (1-8): "))
        if choice.isdigit():
            if choice == '8':
                print("Exit from the application ")
                break
            elif int(choice) < 1 or int(choice) > 8:
                print("Invalid choice. Please select a number between 1 and 8.")
                continue
            solution = search.search_algorithm(problem,choose_strategy(int(choice), goal_state),1, maximum_slope, maximum_depth) 
            if solution:
                show_path(solution)
            else:
                print("No solution")
            print()
        else:
            print("Invalid input. Please enter a number.")
            
        
    


# Import necessary libraries
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import folium

# Function to create the distance matrix
# You need to populate this with real distances between the 276 constituencies
# For simplicity, let's assume we have a smaller subset of distance matrix for testing
def create_data_model():
    data = {}
    # Insert your actual distance matrix here for 276 constituencies (example for 5 constituencies)
    # Replace this matrix with the real data
    data['distance_matrix'] = [
        [0, 20, 42, 35, 25],  # Accra to other places
        [20, 0, 30, 50, 45],  # Region 1 distances
        [42, 30, 0, 28, 33],  # Region 2 distances
        [35, 50, 28, 0, 15],  # Region 3 distances
        [25, 45, 33, 15, 0],  # Region 4 distances
    ]
    data['num_vehicles'] = 1  # Only one traveler (yourself)
    data['depot'] = 0  # Starting point (index of Accra or first constituency)
    return data

# Solve the routing problem using Google OR-Tools
def main_routing():
    # Instantiate the data model
    data = create_data_model()

    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create the routing model
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback for distance
    def distance_callback(from_index, to_index):
        # Returns the distance between the two nodes
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc (the distance callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Set parameters for search (limits, search strategy)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    # Retrieve the solution and print it
    route = []
    if solution:
        print('Objective: {}'.format(solution.ObjectiveValue()))
        index = routing.Start(0)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))  # Append current location (constituency)
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))  # Return to start point (optional)
        print('Optimal Route: {}'.format(route))
    else:
        print('No solution found!')

    return route

# Visualize the route on the map using Folium
def visualize_route(route):
    # Example coordinates for some constituencies, replace with actual coordinates for 276
    coordinates = [
        [5.6037, -0.187],  # Accra (example starting point)
        [6.0723, -0.2682],  # Eastern Region
        [7.8731, -1.054],   # Bono Region
        [8.2011, -0.221],   # Northern Region
        [9.3266, -2.004],   # Upper West Region
    ]

    # Create a folium map centered at Accra
    m = folium.Map(location=coordinates[0], zoom_start=6)

    # Plot each constituency in the optimal route on the map
    for i in route:
        folium.Marker(location=coordinates[i]).add_to(m)
    
    # Draw lines between constituencies to visualize the route
    for i in range(len(route) - 1):
        folium.PolyLine([coordinates[route[i]], coordinates[route[i + 1]]], color="blue", weight=2.5).add_to(m)

    # Save map to an HTML file
    m.save('ghana_constituencies_route.html')

    print("Map has been saved as 'ghana_constituencies_route.html'")

if __name__ == '__main__':
    # Step 1: Solve the routing problem to get the optimal route
    optimal_route = main_routing()

    # Step 2: Visualize the route on a map
    visualize_route(optimal_route)

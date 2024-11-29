import random
import time
import csv
from itertools import product
from graph_utils import generate_random_graph, save_graph, load_graph


# EXHAUSTIVE SEARCH with tracking of operations and configurations tested
def is_valid_coloring(graph, coloring):
    basic_operations = 0
    for u, v in graph.edges():
        basic_operations += 1
        if coloring[u] == coloring[v]:
            return False, basic_operations
    return True, basic_operations

def exhaustive_chromatic_number(graph):
    n = len(graph.nodes())
    basic_operations = 0
    configurations_tested = 0   

    for num_colors in range(1, n + 1):
        for coloring in product(range(num_colors), repeat=n):
            configurations_tested += 1
            is_valid, edge_operations = is_valid_coloring(graph, coloring)  # Check if valid and get edge operations
            basic_operations += edge_operations    
            if is_valid:                            # If the coloring is valid
                return num_colors, basic_operations, configurations_tested
    return n, basic_operations, configurations_tested  # Worst case


# GREEDY HEURISTIC with tracking of operations and configurations tested
def greedy_chromatic_number(graph):
    n = len(graph.nodes())
    coloring = {}
    basic_operations = 0
    configurations_tested = 0

    vertices = sorted(graph.nodes(), key=lambda x: graph.degree[x], reverse=True)
    
    for vertex in vertices:
        neighbor_colors = {coloring[neighbor] for neighbor in graph.neighbors(vertex) if neighbor in coloring}
        color = 0
        while color in neighbor_colors:
            color += 1
            basic_operations += 1  # Checking if color is in neighbor_colors is a basic operation

        coloring[vertex] = color
        configurations_tested += 1  # Each assignment is considered a configuration
    
    chromatic_number = max(coloring.values()) + 1
    return chromatic_number, basic_operations, configurations_tested


def random_greedy_chromatic_number(graph, trials=30):
    basic_operations = 0
    configurations_tested = 0
    
    best_chromatic_number = float('inf')  # Initialize with a large value
    tested_orders = set()  # To store unique vertex orders
    vertices = list(graph.nodes())

    for _ in range(trials):
        # Generate a new unique vertex order
        while True:
            random.shuffle(vertices)
            vertex_order = tuple(vertices)  # Convert list to tuple for set operations
            if vertex_order not in tested_orders:
                tested_orders.add(vertex_order)
                break  # Found a new unique order

        # Perform greedy coloring on the randomized order
        coloring = {}
        for vertex in vertices:
            neighbor_colors = {coloring[neighbor] for neighbor in graph.neighbors(vertex) if neighbor in coloring}
            color = 0
            while color in neighbor_colors:
                color += 1
                basic_operations += 1

            coloring[vertex] = color
            configurations_tested += 1  # Each assignment is considered a configuration
            

        # Compute chromatic number for this trial
        chromatic_number = max(coloring.values()) + 1
        best_chromatic_number = min(best_chromatic_number, chromatic_number)

    return best_chromatic_number, basic_operations, configurations_tested




def main():
    edges = [12.5, 25, 50, 75]
    trials = 1
    maxVertices = 500
    graph_folder = "graphs"  
    exhaustive_max_vertices = 10

    with open('results/greedy_results.csv', mode='w', newline='') as greedy_file, \
         open('results/exhaustive_results.csv', mode='w', newline='') as exhaustive_file, \
         open('results/random_greedy_results.csv', mode='w', newline='') as random_greedy_file:
        
        greedy_writer = csv.writer(greedy_file)
        exhaustive_writer = csv.writer(exhaustive_file)
        random_greedy_writer = csv.writer(random_greedy_file)

        # CSV headers
        headers = ['Vertices', 'Edge %', 'Chromatic Number', 'Exec Time', 
                   'Basic Operations', 'Configurations Tested', 'Precision']
        greedy_writer.writerow(headers)
        exhaustive_writer.writerow(headers[:-1])  # Exhaustive doesn't need precision
        random_greedy_writer.writerow(headers)


        for num_vertices in range(4, maxVertices + 1):
            print("Vertices: "+str(num_vertices))
            
            for edge_percentage in edges:

                # Graph filename based on parameters
                graph_filename = f"graph_{num_vertices}_vertices_{int(edge_percentage)}_edges.pkl"
                G = load_graph(graph_folder, graph_filename)  # Try loading the graph

                if G is None:
                    G = generate_random_graph(num_vertices, edge_percentage / 100)  # Generate the graph
                    save_graph(G, graph_folder, graph_filename)  # Save the graph


                num_edges = G.number_of_edges()  # Get the number of edges
                edges_formatted = f"{num_edges} ({edge_percentage}%)"

                # Greedy Heuristic 
                greedy_times = []
                greedy_basic_ops = 0
                greedy_configs = 0
                chromatic_num_greedy = None
                
                for _ in range(trials):
                    start = time.time()
                    chromatic_num_greedy, basic_ops_greedy, configs_greedy = greedy_chromatic_number(G)
                    end = time.time()
                    greedy_times.append((end - start) * 10**3)
                    greedy_basic_ops += basic_ops_greedy
                    greedy_configs += configs_greedy
                
                avg_greedy_time = sum(greedy_times) / trials
                avg_greedy_ops = greedy_basic_ops // trials
                avg_greedy_configs = greedy_configs // trials


                # Random Greedy Heuristic 
                random_greedy_times = []
                random_greedy_basic_ops = 0
                random_greedy_configs = 0
                chromatic_num_random_greedy = None
                
                for _ in range(trials):
                    start = time.time()
                    chromatic_num_random_greedy, basic_ops_random_greedy, configs_random_greedy = random_greedy_chromatic_number(G, min(500, 6*num_vertices))
                    end = time.time()
                    random_greedy_times.append((end - start) * 10**3)
                    random_greedy_basic_ops += basic_ops_random_greedy
                    random_greedy_configs += configs_random_greedy
                
                avg_random_greedy_time = sum(random_greedy_times) / trials
                avg_random_greedy_ops = random_greedy_basic_ops // trials
                avg_random_greedy_configs = random_greedy_configs // trials


                # Exhaustive Search (only for smaller instances)
                if num_vertices <= exhaustive_max_vertices:
                    exhaustive_times = []
                    exhaustive_basic_ops = 0
                    exhaustive_configs = 0
                    chromatic_num_exhaustive = None

                    for _ in range(trials):
                        start = time.time()
                        chromatic_num_exhaustive, basic_ops_exhaustive, configs_exhaustive = exhaustive_chromatic_number(G)
                        end = time.time()
                        exhaustive_times.append((end - start) * 10**3)
                        exhaustive_basic_ops += basic_ops_exhaustive
                        exhaustive_configs += configs_exhaustive

                    avg_exhaustive_time = sum(exhaustive_times) / trials
                    avg_exhaustive_ops = exhaustive_basic_ops // trials
                    avg_exhaustive_configs = exhaustive_configs // trials
                    exhaustive_writer.writerow([num_vertices, edges_formatted, chromatic_num_exhaustive, 
                                                f"{avg_exhaustive_time:.4f}", avg_exhaustive_ops, avg_exhaustive_configs])

                    # Calculate precision
                    greedy_precision = abs(chromatic_num_exhaustive - chromatic_num_greedy)
                    random_greedy_precision = abs(chromatic_num_exhaustive - chromatic_num_random_greedy)
                else:
                    greedy_precision = None         # Precision not applicable when exhaustive not run
                    random_greedy_precision = None  # Precision not applicable when exhaustive not run


                # Write results 
                greedy_writer.writerow([num_vertices, edges_formatted, chromatic_num_greedy, f"{avg_greedy_time:.4f}", avg_greedy_ops, avg_greedy_configs, greedy_precision])
                random_greedy_writer.writerow([num_vertices, edges_formatted, chromatic_num_random_greedy, f"{avg_random_greedy_time:.4f}", avg_random_greedy_ops, avg_random_greedy_configs, random_greedy_precision])

if __name__ == "__main__":
    main()

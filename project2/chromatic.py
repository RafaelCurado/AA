import time
import csv
import random
from itertools import product
from graph_utils import generate_random_graph, save_graph, load_graph

# This seed is just for the random algorithm and not for the graph generation, should i keep it??
studentN = 103199
random.seed(studentN)

# EXAUSTIVE SEARCH
def is_valid_coloring(graph, coloring):
    for u, v in graph.edges():
        if coloring[u] == coloring[v]:
            return False
    return True 

def exhaustive_chromatic_number(graph):
    n = len(graph.nodes())

    for num_colors in range(1, n + 1):
        for coloring in product(range(num_colors), repeat=n):
            if is_valid_coloring(graph, coloring):
                return num_colors  
    return n  # Worst case -> chromatic number = N of vertices


# GREEDY HEURISTIC
def greedy_chromatic_number(graph):
    n = len(graph.nodes())
    coloring = {}
    
    # Sort vertices by descending degree = n of edges
    vertices = sorted(graph.nodes(), key=lambda x: graph.degree[x], reverse=True)
    
    for vertex in vertices:
        neighbor_colors = {coloring[neighbor] for neighbor in graph.neighbors(vertex) if neighbor in coloring}
        
        # Find the smallest available color that isn't used by neighbors
        color = 0
        while color in neighbor_colors:
            color += 1
        
        coloring[vertex] = color  # Assign the found color
    
    # Max color used + 1
    chromatic_number = max(coloring.values()) + 1
    return chromatic_number


def randomized_greedy_chromatic_number(graph, trials=10):

    best_chromatic_number = float('inf')  # Initialize with a large value

    for _ in range(trials):
        # Randomize the vertex order
        vertices = list(graph.nodes())
        random.shuffle(vertices)

        # Perform greedy coloring on the randomized order
        coloring = {}
        for vertex in vertices:
            neighbor_colors = {coloring[neighbor] for neighbor in graph.neighbors(vertex) if neighbor in coloring}
            color = 0
            while color in neighbor_colors:
                color += 1
            coloring[vertex] = color

        # Compute chromatic number for this trial
        chromatic_number = max(coloring.values()) + 1
        best_chromatic_number = min(best_chromatic_number, chromatic_number)

    return best_chromatic_number


def main():
    edges = [12.5, 25, 50, 75]
    trials = 1
    maxVertices = 100
    graph_folder = "graphs"  
    exhaustive_max_vertices = 10

    with open('results/greedy_exectimes.csv', mode='w', newline='') as greedy_file, \
         open('results/exhaustive_exectimes.csv', mode='w', newline='') as exhaustive_file, \
         open('results/random-greedy_exectimes.csv', mode='w', newline='') as random_greedy_file:

        greedy_writer = csv.writer(greedy_file)
        exhaustive_writer = csv.writer(exhaustive_file)
        random_greedy_writer = csv.writer(random_greedy_file)

        headers = ['Vertices / Edge %'] + [f'{edge}%' for edge in edges]
        greedy_writer.writerow(headers)
        exhaustive_writer.writerow(headers)
        random_greedy_writer.writerow(headers)

        for num_vertices in range(4, maxVertices + 1):  

            greedy_row = [num_vertices]
            exhaustive_row = [num_vertices]
            random_greedy_row = [num_vertices]

            for possible_edges in edges:

                greedy_times = []
                exhaustive_times = []
                random_greedy_times = []

                # Graph filename based on parameters
                graph_filename = f"graph_{num_vertices}_vertices_{int(possible_edges)}_edges.pkl"
                G = load_graph(graph_folder, graph_filename)  # Try loading the graph

                if G is None:
                    G = generate_random_graph(num_vertices, possible_edges / 100)  # Generate the graph
                    save_graph(G, graph_folder, graph_filename)  # Save the graph

                for trial in range(trials):
                    # Greedy
                    start = time.time()
                    chromatic_num_greedy = greedy_chromatic_number(G)
                    end = time.time()
                    greedy_times.append((end - start) * 10**3)

                    # Exhaustive Search (max 11 vertices)
                    if num_vertices <= exhaustive_max_vertices and possible_edges <= 50:
                        start = time.time()
                        chromatic_num_exhaustive = None
                        chromatic_num_exhaustive = exhaustive_chromatic_number(G)
                        end = time.time()
                        exhaustive_times.append((end - start) * 10**3)

                    # Random Greedy
                    start = time.time()
                    chromatic_num_random_greedy = randomized_greedy_chromatic_number(G, 10)
                    end = time.time()
                    random_greedy_times.append((end - start) * 10**3)


                avg_greedy_time = sum(greedy_times) / trials
                greedy_row.append(avg_greedy_time)

                if num_vertices <= exhaustive_max_vertices or possible_edges <= 50:
                    avg_exhaustive_time = sum(exhaustive_times) / trials
                    exhaustive_row.append(avg_exhaustive_time)

                avg_random_greedy_time = sum(random_greedy_times) / trials
                random_greedy_row.append(avg_random_greedy_time)

                print(f"\n\n\n({num_vertices} vertices, {possible_edges}% edges)")

                print(f"\nGreedy Chromatic Number: "+str(chromatic_num_greedy))
                print(f"Greedy Execution Time: {avg_greedy_time:.4f} ms")

                if num_vertices <= exhaustive_max_vertices or possible_edges <= 50:
                    print(f"\nExhaustive Chromatic Number: "+str(chromatic_num_exhaustive))
                    print(f"Exhaustive Execution Time: {avg_exhaustive_time:.4f} ms")

                print(f"\nRandom Greedy Chromatic Number: "+str(chromatic_num_random_greedy))
                print(f"Random Greedy Execution Time: {avg_random_greedy_time:.4f} ms")

            # Write rows to CSV files
            greedy_writer.writerow(greedy_row)
            exhaustive_writer.writerow(exhaustive_row)
            random_greedy_writer.writerow(random_greedy_row)
            

if __name__ == "__main__":
    main()

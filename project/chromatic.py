import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import csv
from itertools import combinations, product

studentN = 103199
random.seed(studentN)


def generate_unique_points(num_points, min_distance=10):
    points = set()
    while len(points) < num_points:
        x = random.randint(1, 1000)
        y = random.randint(1, 1000)
        point = (x, y)

        # Ensure points are unique and not too close to each other
        if all(np.linalg.norm(np.array(point) - np.array(p)) >= min_distance for p in points):
            points.add(point)

    return list(points)



def generate_random_graph(num_vertices, edge_percentage):
    points = generate_unique_points(num_vertices)
    G = nx.Graph()
    
    for i, point in enumerate(points):
        G.add_node(i, pos=point)
    
    max_edges = num_vertices * (num_vertices - 1) // 2
    num_edges = int(max_edges * edge_percentage)

    possible_edges = list(combinations(range(num_vertices), 2))
    random_edges = random.sample(possible_edges, num_edges)

    G.add_edges_from(random_edges)
    
    return G, points



def visualize_graph(G, coloring, filename):
    plt.figure(figsize=(8, 6))
    
    pos = nx.get_node_attributes(G, 'pos')

    colors = [
        'red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 
        'gray', 'cyan', 'magenta', 'lime', 'olive', 'navy', 'maroon', 'teal',
        'gold', 'violet', 'turquoise', 'indigo', 'khaki', 'plum', 'salmon', 'tan'
    ]   


    node_colors = [colors[coloring[i]] for i in G.nodes()]

    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=12, edge_color='gray')
    
    plt.savefig(filename)
    plt.show()


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
                return num_colors, coloring  
    return n, None  # Worst case -> chromatic number = N of vertices


# GREEDY HEURISTIC

def greedy_chromatic_number(graph):
    n = len(graph.nodes())
    coloring = {}
    
    # Sort vertices by descending degree - N of edges
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
    return chromatic_number, coloring




def main():
    edges = [12.5, 25, 50, 75]
    trials = 1

    with open('greedy_results.csv', mode='w', newline='') as greedy_file, open('exhaustive_results.csv', mode='w', newline='') as exhaustive_file:
        
        greedy_writer = csv.writer(greedy_file)
        exhaustive_writer = csv.writer(exhaustive_file)

        headers = ['Vertices / Edge %'] + [f'{edge}%' for edge in edges]
        greedy_writer.writerow(headers)
        exhaustive_writer.writerow(headers)

        for num_vertices in range(4, 12):

            greedy_row = [num_vertices]
            exhaustive_row = [num_vertices]

            for possible_edges in edges:

                greedy_times = []
                exaustive_times = []

                G, points = generate_random_graph(num_vertices, possible_edges/100) # calculate points

                for trial in range(trials):

                    start = time.time()    
                    chromatic_num_greedy, coloring = greedy_chromatic_number(G)
                    end = time.time()
                    greedy_times.append((end-start)*10**3)


                    start = time.time()
                    chromatic_num_exhaustive, coloring = exhaustive_chromatic_number(G)
                    end = time.time()
                    exaustive_times.append((end-start)*10**3)

                avg_greedy_time = sum(greedy_times)/trials
                avg_exhaustive_time = sum(exaustive_times)/trials

                print(f"\nGreedy Chromatic Number ({num_vertices} vertices, {possible_edges}% edges): "+str(chromatic_num_greedy))
                print(f"Greedy Execution Time: {avg_greedy_time:.4f} ms")
                print(f"Exaustive Chromatic Number ({num_vertices} vertices, {possible_edges}% edges): "+str(chromatic_num_exhaustive))
                print(f"Exhaustive Execution Time: {avg_exhaustive_time:.4f} ms")

                greedy_row.append(avg_greedy_time)
                exhaustive_row.append(avg_exhaustive_time)

                #visualize_graph(G, coloring, "graph_visualization.png")

            greedy_writer.writerow(greedy_row)
            exhaustive_writer.writerow(exhaustive_row)

        #print("Points: ", points)  
        #visualize_graph(G, coloring, "graph_visualization.png")
        #nx.write_graphml(G, "graph.graphml")



if __name__ == "__main__":
    main()

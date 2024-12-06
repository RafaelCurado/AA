from io import StringIO
import random
import networkx as nx
import numpy as np
import os
import pickle
from itertools import combinations, product

# studentN = 103199
# random.seed(studentN)

#  Not using seed anymore because it was used in the 1st project 
#   for the graphs generation and now it would have different values
#   because in the 2st project random() is used more often


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
    
    return G


def save_graph(graph, folder, filename):
    os.makedirs(folder, exist_ok=True)  # Ensure the folder exists
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as f:
        pickle.dump(graph, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_graph(folder, filename):
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return None
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except (EOFError, pickle.UnpicklingError):
        print(f"Error: Corrupted file {filepath}.")
        return None
    


def load_webgraph(graph_folder, filename):
    """
    Load a graph from either the Facebook or SW dataset based on the folder structure.

    :param graph_folder: Directory where the graphs are stored.
    :param filename: The filename to load the corresponding graph.
    :return: NetworkX graph object or None if file not found.
    """
    # Check if the graph is from Facebook or SW by examining the subdirectory of the folder
    if os.path.exists(f"{graph_folder}/facebook/{filename}"):  # Check if the file is in the facebook directory
        edge_file = f"{graph_folder}/facebook/{filename}"
        try:
            # Read the edge file and create the graph
            G = nx.read_edgelist(edge_file, nodetype=int)  # Reads the edge list and converts nodes to integers
        except FileNotFoundError:
            print(f"Edge file {edge_file} not found.")
            return None
    elif os.path.exists(f"{graph_folder}/sw/{filename}"):  # Check if the file is in the sw directory
        edge_file = f"{graph_folder}/sw/{filename}"
        try:
            # Read the SW graph file, skipping the first 4 lines
            with open(edge_file, 'r') as f:
                lines = f.readlines()[4:]  # Skip first 4 lines

            # Write the remaining lines to a temporary file-like object for parsing
            temp_file = StringIO("".join(lines))

            # Use NetworkX to read the edge list
            G = nx.read_edgelist(temp_file, nodetype=int)
        except FileNotFoundError:
            print(f"Error: File {edge_file} not found.")
            G = None
        except ValueError:
            print(f"Error: File {edge_file} format is invalid. Ensure it contains valid edge definitions.")
            G = None
    else:
        print(f"Error: {filename} is not found in either 'facebook' or 'sw' subdirectories.")
        G = None

    return G



# graph_folder = "graphs_web"
# filename = "0.edges"  # Replace with the actual filename

# graph = load_graph(graph_folder, filename)
# if graph:
#     print(f"Loaded graph with {len(graph.nodes())} nodes and {len(graph.edges())} edges.")
# else:
#     print("Failed to load graph.")





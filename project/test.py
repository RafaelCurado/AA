import matplotlib.pyplot as plt

import networkx as nx
from itertools import product

def is_valid_coloring(graph, coloring):
    """Check if the given coloring is valid (no adjacent vertices share the same color)."""
    for u, v in graph.edges():
        if coloring[u] == coloring[v]:
            return False
    return True

def exhaustive_chromatic_number(graph):
    """Find the chromatic number of a graph using exhaustive search."""
    n = len(graph.nodes())
    
    # Try coloring the graph with increasing numbers of colors
    for num_colors in range(1, n + 1):
        # Generate all possible colorings for the given number of colors
        # Each node can be assigned a color in the range [0, num_colors - 1]
        for coloring in product(range(num_colors), repeat=n):
            # If a valid coloring is found, return the number of colors used
            if is_valid_coloring(graph, coloring):
                return num_colors
    return n  # Worst case, chromatic number is equal to the number of vertices

def main():
    # Example: Create a sample graph
    G = nx.erdos_renyi_graph(5, 0.5)  # 5 nodes with random edges
    
    # Find and print the chromatic number
    chromatic_num = exhaustive_chromatic_number(G)
    print(f"The chromatic number of the graph is: {chromatic_num}")

    # Optionally visualize the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12, edge_color='gray')
    plt.show()

if __name__ == "__main__":
    main()

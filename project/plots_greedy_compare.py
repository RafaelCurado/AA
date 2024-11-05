import matplotlib.pyplot as plt
import csv

def load_data(filename):
    """Helper function to load data from CSV files."""
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip headers
        for row in reader:
            data.append([float(value) if i > 0 else int(value) for i, value in enumerate(row)])
    return headers, data


def plot_greedy_comparison():
    # Load data for both greedy algorithms
    headers, top_data = load_data('data/greedy_top_results.csv')
    _, bottom_data = load_data('data/greedy_bottom_results.csv')

    # Vertices / Edge %
    x_labels = [f"{row[0]} vertices" for row in top_data]
    edge_percentages = headers[1:]  # Skip "Vertices / Edge %"

    # Plot comparison for each edge percentage
    plt.figure(figsize=(12, 8))

    for i, edge_percentage in enumerate(edge_percentages, start=1):
        top_times = [row[i] for row in top_data]
        bottom_times = [row[i] for row in bottom_data]

        plt.plot(x_labels, top_times, marker='o', label=f'Greedy Top ({edge_percentage}%)')
        plt.plot(x_labels, bottom_times, marker='s', linestyle='--', label=f'Greedy Bottom ({edge_percentage}%)')

    plt.xlabel("Graph Configuration (Vertices)")
    plt.ylabel("Average Execution Time (ms)")
    plt.title("Comparison of Greedy Top and Bottom Algorithms")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.yscale('log')
    
    plt.savefig("plots/greedy_comparison_plot.png")
    plt.show()


if __name__ == "__main__":
    plot_greedy_comparison()

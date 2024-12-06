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
    headers, top_data = load_data('exec_times/greedy_top_times.csv')
    _, bottom_data = load_data('exec_times/greedy_bottom_times.csv')

    # Use only the first 100 points and select every 5th row (interval of 5)
    top_data_sampled = top_data[:600:80]
    bottom_data_sampled = bottom_data[:600:80]

    # Vertices / Edge %
    x_labels = [f"{row[0]}" for row in top_data_sampled]
    edge_percentages = headers[1:]  # Skip "Vertices / Edge %"

    # Plot comparison for each edge percentage
    plt.figure(figsize=(10, 6))

    for i, edge_percentage in enumerate(edge_percentages, start=1):
        top_times = [row[i] for row in top_data_sampled]
        bottom_times = [row[i] for row in bottom_data_sampled]

        plt.plot(x_labels, top_times, marker='o', label=f'Greedy Top ({edge_percentage}%)')
        plt.plot(x_labels, bottom_times, marker='s', linestyle='--', label=f'Greedy Bottom ({edge_percentage}%)')

    plt.xlabel("Number of vertices")
    plt.ylabel("Average Execution Time (ms)")
    plt.title("Comparison of Greedy Top and Bottom Algorithms")
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.tight_layout()
    # plt.yscale('log')
    
    plt.savefig("plots/greedy_comparison_plot.png")
    plt.show()


if __name__ == "__main__":
    plot_greedy_comparison()

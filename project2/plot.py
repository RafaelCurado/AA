import pandas as pd
import matplotlib.pyplot as plt

# Load the two CSV files (replace 'algorithm1.csv' and 'algorithm2.csv' with your actual file paths)
df1 = pd.read_csv('results/greedy_results.csv')
df2 = pd.read_csv('results/random_greedy_results.csv')

# Function to process the data and extract chromatic number per edge density and vertices
def process_data(df):
    # Print the raw 'Edge %' column to inspect how it's loaded
    print("Raw 'Edge %' values before cleaning:")
    print(df['Edge %'].head(20))  # Print first 20 rows to understand the format

    # Clean the 'Edge %' column by extracting percentage using regex and converting to numeric
    df['Edge %'] = df['Edge %'].str.extract(r'(\d+\.\d+|\d+)\s?\%')  # Regex to extract numbers with optional decimal
    df['Edge %'] = pd.to_numeric(df['Edge %'], errors='coerce')  # Convert to numeric, invalid entries become NaN

    # Print unique edge densities to verify the correct values
    print("Unique edge densities found in the data:", df['Edge %'].unique())

    return df

# Process data for both algorithms
df1 = process_data(df1)
df2 = process_data(df2)

# Now let's filter and process the data for each edge density value
edge_densities = [12.5, 25, 50, 75]
chromatic_numbers1 = {edge_density: [] for edge_density in edge_densities}
chromatic_numbers2 = {edge_density: [] for edge_density in edge_densities}

# Extract chromatic number for each edge density and vertices
for edge_density in edge_densities:
    # For algorithm 1 (Greedy)
    subset1 = df1[df1['Edge %'] == edge_density]
    if not subset1.empty:  # Check if there's data for the current edge density
        chromatic_numbers1[edge_density] = subset1.groupby('Vertices')['Chromatic Number'].max()

    # For algorithm 2 (Random Greedy)
    subset2 = df2[df2['Edge %'] == edge_density]
    if not subset2.empty:  # Check if there's data for the current edge density
        chromatic_numbers2[edge_density] = subset2.groupby('Vertices')['Chromatic Number'].max()

# Print out the chromatic numbers for each edge density to verify
for edge_density in edge_densities:
    print(f"Greedy - Edge Density {edge_density}% Chromatic Numbers:")
    print(chromatic_numbers1[edge_density])
    print(f"Random Greedy - Edge Density {edge_density}% Chromatic Numbers:")
    print(chromatic_numbers2[edge_density])

# Plotting the results
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Titles and edge density values for plotting
axes = axs.ravel()  # Flatten the 2D axes array

# Plot data for both algorithms
for i, edge_density in enumerate(edge_densities):
    ax = axes[i]

    # Check if there is data for the current edge density in Greedy
    if not chromatic_numbers1[edge_density].empty:
        # Downsample by selecting every 10th vertex (indexing starts at 0)
        downsampled_x = chromatic_numbers1[edge_density].index[::10]  # Every 10th index
        downsampled_y = chromatic_numbers1[edge_density].values[::10]  # Corresponding chromatic numbers
        
        ax.plot(downsampled_x, downsampled_y, label='Greedy', marker='o', color='blue', linestyle='-', markersize=6)

    # Check if there is data for the current edge density in Random Greedy
    if not chromatic_numbers2[edge_density].empty:
        # Downsample by selecting every 10th vertex (indexing starts at 0)
        downsampled_x = chromatic_numbers2[edge_density].index[::10]  # Every 10th index
        downsampled_y = chromatic_numbers2[edge_density].values[::10]  # Corresponding chromatic numbers
        
        ax.plot(downsampled_x, downsampled_y, label='Random Greedy', marker='x', color='red', linestyle='--', markersize=6)

    # Set labels and title
    ax.set_title(f'Edge Density = {edge_density}%')
    ax.set_xlabel('Number of Vertices')
    ax.set_ylabel('Chromatic Number')

    # Only show legend if there is data for both algorithms
    if not chromatic_numbers1[edge_density].empty or not chromatic_numbers2[edge_density].empty:
        ax.legend()

# Adjust layout for better spacing
plt.tight_layout()

# Show the plot
plt.show()

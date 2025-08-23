import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Hardcoded grid size and range
n, m = 10, 15   # Grid size (rows, cols)
MIN_VAL, MAX_VAL = 1, 40   # Range of values

def generate_grid(n, m, min_val, max_val):
    """Generate an n x m grid randomly filled with numbers in [min_val, max_val]."""
    return [[random.randint(min_val, max_val) for _ in range(m)] for _ in range(n)]

def show_grid(grid):
    """Show the grid with green heatmap background + numbers and borders."""
    n, m = len(grid), len(grid[0])

    # Convert grid to numpy array
    grid_array = np.array(grid)

    # Create custom colormap from light green to dark green
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["#d4f7d4", "#004d00"])

    plt.figure(figsize=(8, 6))
    plt.imshow(grid_array, cmap=cmap, vmin=MIN_VAL, vmax=MAX_VAL, aspect='equal')

    # Add grid lines
    plt.grid(which='major', color='black', linewidth=1.2)
    plt.xticks(np.arange(-0.5, m, 1), [])
    plt.yticks(np.arange(-0.5, n, 1), [])
    plt.gca().set_xticks(np.arange(-.5, m, 1), minor=True)
    plt.gca().set_yticks(np.arange(-.5, n, 1), minor=True)
    plt.grid(which="minor", color="black", linestyle='-', linewidth=1)

    # Annotate values in each cell (always black for readability)
    for i in range(n):
        for j in range(m):
            plt.text(j, i, str(grid[i][j]), ha='center', va='center', fontsize=12, color='black')

    plt.title(f"Random {n}x{m} Grid with Heatmap [{MIN_VAL}, {MAX_VAL}]")
    plt.show()

if __name__ == "__main__":
    grid = generate_grid(n, m, MIN_VAL, MAX_VAL)
    print("Generated Grid:")
    for row in grid:
        print(row)
    show_grid(grid)

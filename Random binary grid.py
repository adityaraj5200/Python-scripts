import random
import matplotlib.pyplot as plt
import numpy as np

# Hardcoded grid size
n, m = 10, 15   # <-- change these values as needed

def generate_grid(n, m):
    """Generate an n x m grid randomly filled with 0s and 1s."""
    return [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]

def show_grid(grid):
    """Show the grid with a clean UI."""
    plt.figure(figsize=(8, 6))
    cmap = plt.cm.get_cmap('coolwarm', 2)  # Blue for 0, Red for 1
    plt.imshow(grid, cmap=cmap, aspect='equal')

    # Add grid lines
    plt.grid(which='major', color='black', linewidth=1.2)
    plt.xticks(np.arange(-0.5, m, 1), [])
    plt.yticks(np.arange(-0.5, n, 1), [])
    plt.gca().set_xticks(np.arange(-.5, m, 1), minor=True)
    plt.gca().set_yticks(np.arange(-.5, n, 1), minor=True)
    plt.grid(which="minor", color="black", linestyle='-', linewidth=1)

    # Annotate values in each cell
    for i in range(n):
        for j in range(m):
            plt.text(j, i, str(grid[i][j]), ha='center', va='center', fontsize=12, color='white')

    plt.title(f"Random {n}x{m} Grid of 0s and 1s")
    plt.show()

if __name__ == "__main__":
    grid = generate_grid(n, m)
    print("Generated Grid:")
    for row in grid:
        print(row)
    show_grid(grid)

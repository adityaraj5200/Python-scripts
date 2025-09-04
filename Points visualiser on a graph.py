import matplotlib.pyplot as plt

def plot_points(points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]

    plt.figure(figsize=(7,7))
    plt.scatter(x_coords, y_coords, 
                c="royalblue", 
                s=150, 
                edgecolors="black", 
                linewidths=1.2, 
                alpha=0.8, 
                marker="o")

    # Annotate each point with index + coordinates
    for idx, (x,y) in enumerate(points):
        plt.text(x+0.15, y+0.15, f"{idx}:({x},{y})", 
                fontsize=10, 
                color="darkred", 
                weight="bold")

    # Grid and axes styling
    plt.xlabel("X-axis", fontsize=12, weight="bold")
    plt.ylabel("Y-axis", fontsize=12, weight="bold")
    plt.title("Point Visualization", fontsize=14, weight="bold", color="navy")

    plt.grid(True, linestyle="--", alpha=0.5)
    plt.gca().set_facecolor("#f8f9fa")  # light background
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 🔹 Replace with your points
    points =[[0,5],[6,1],[4,5]]

    plot_points(points)

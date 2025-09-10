import random
import matplotlib.pyplot as plt

def generate_random_array(min_size=5, max_size=20, min_val=1, max_val=100):
    """Generate a random array with random size and values."""
    size = random.randint(min_size, max_size)
    array = [random.randint(min_val, max_val) for _ in range(size)]
    return array

def generate_random_multiples_of_10(min_size=5, max_size=20, min_val=1, max_val=10):
    """Generate a random array of values and multiply each by 10."""
    base_array = generate_random_array(min_size, max_size, min_val, max_val)
    multiples_array = [val * 10 for val in base_array]
    return multiples_array

def visualize_array(array):
    """Visualize the array as a vertical bar chart."""
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(array)), array, color='skyblue')
    plt.title("Random Array Visualization by Aditya")
    plt.xlabel("Index")
    plt.ylabel("Value (Height)")
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    for i, val in enumerate(array):
        plt.text(i, val + 1, str(val), ha='center', fontsize=9)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    minsize = 50
    maxsize = 50
    minval = 0hello 342
    hello 343
    hello 344
    hello 345
    hello 346
    he
    maxval = 50
    random_array = generate_random_array(minsize, maxsize, minval, maxval)
    print(random_array)
    multiples_of_10_array = generate_random_multiples_of_10()
    # hardcoded_array = [3,4,3,2,1,2,3,4,3,2,1]

    visualize_array(random_array)
    # visualize_array(hardcoded_array)
    # visualize_array(multiples_of_10_array)

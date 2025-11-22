import os

def generate_tree(root_dir, prefix=""):
    entries = sorted(os.listdir(root_dir))
    tree_str = ""
    pointers = ["├── ", "└── "]
    
    for index, entry in enumerate(entries):
        path = os.path.join(root_dir, entry)
        connector = pointers[0] if index < len(entries) - 1 else pointers[1]

        tree_str += prefix + connector + entry + "\n"

        if os.path.isdir(path):
            extension = "│   " if index < len(entries) - 1 else "    "
            tree_str += generate_tree(path, prefix + extension)

    return tree_str


if __name__ == "__main__":
    root = os.getcwd()  # use current directory as root
    tree_output = os.path.basename(root) + "/\n"
    tree_output += generate_tree(root)

    # Save to output.txt
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(tree_output)

    print("Directory structure saved to output.txt")

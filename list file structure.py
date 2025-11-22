import os

def print_tree(root_path, file, indent_level=0):
    try:
        items = os.listdir(root_path)
    except PermissionError:
        file.write(" " * (indent_level * 4) + f"[ACCESS DENIED] {root_path}\n")
        return

    for item in sorted(items):
        item_path = os.path.join(root_path, item)

        # Skip "target" or any dot-folder
        if os.path.isdir(item_path) and (item.lower() == "target" or item.startswith(".")):
            file.write(" " * (indent_level * 4) + f"{item} [skipped]\n")
            continue

        file.write(" " * (indent_level * 4) + item + "\n")

        if os.path.isdir(item_path):
            print_tree(item_path, file, indent_level + 1)

if __name__ == "__main__":
    root = os.getcwd()  # Start at current directory
    output_path = "output.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Directory structure for: {root}\n\n")
        print_tree(root, f)

    print(f"Directory tree written to {output_path}")

import os

def replace_and_numberify(input_file="input.txt", output_file="output.txt"):
    # Get directory of the script itself
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, input_file)
    output_path = os.path.join(base_dir, output_file)

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    counter = 1
    result = ""
    i = 0
    while i < len(text):
        if text.startswith("numberify_it", i):
            result += str(counter)
            counter += 1
            i += len("numberify_it")
        else:
            result += text[i]
            i += 1

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)


if __name__ == "__main__":
    replace_and_numberify()
    print("✅ Replacement complete! Check output.txt")

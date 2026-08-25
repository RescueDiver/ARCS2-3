import json
import os

# ------------------------------
# Load dataset
# ------------------------------
file_path = os.path.join(os.path.dirname(__file__), "small.json")

with open(file_path, "r", encoding="utf-8") as f:
    tasks = json.load(f)

print(f"Loaded dataset with {len(tasks)} tasks.\n")

# ------------------------------
# Tiny rule set
# ------------------------------

def identity(grid):
    return [row[:] for row in grid]

def flip_horizontal(grid):
    return [row[::-1] for row in grid]

def flip_vertical(grid):
    return grid[::-1]

def rotate_90(grid):
    return [list(row) for row in zip(*grid[::-1])]

def solid_fill(grid, color):
    h = len(grid)
    w = len(grid[0])
    return [[color for _ in range(w)] for _ in range(h)]

# ------------------------------
# Rule detector for very small problems
# ------------------------------

def detect_rule(train_input, train_output):
    # identity
    if identity(train_input) == train_output:
        return ("identity", identity)

    # flip horizontal
    if flip_horizontal(train_input) == train_output:
        return ("flip_horizontal", flip_horizontal)

    # flip vertical
    if flip_vertical(train_input) == train_output:
        return ("flip_vertical", flip_vertical)

    # rotate 90
    if rotate_90(train_input) == train_output:
        return ("rotate_90", rotate_90)

    # solid fill only if output is one color
    flat = [v for row in train_output for v in row]
    if len(set(flat)) == 1:
        color = flat[0]
        if solid_fill(train_input, color) == train_output:
            return (f"solid_fill_{color}", lambda g, c=color: solid_fill(g, c))

    return (None, None)

# ------------------------------
# Solve one task using first train example only
# ------------------------------

def solve_task(task):
    train = task.get("train", [])
    test = task.get("test", [])

    if not train:
        return None, None

    first_example = train[0]
    rule_name, rule_fn = detect_rule(first_example["input"], first_example["output"])

    if rule_fn is None:
        return None, None

    predictions = []
    for ex in test:
        predictions.append(rule_fn(ex["input"]))

    return rule_name, predictions

# ------------------------------
# Evaluate
# ------------------------------

total = 0
correct = 0
skipped = 0

for i, task in enumerate(tasks):
    task_id = f"task_{i}"
    rule_name, predictions = solve_task(task)

    if rule_name is None:
        print(f"Task {task_id} -> skipped")
        skipped += len(task.get("test", []))
        continue

    print(f"Task {task_id} -> using {rule_name}")

    for pred, ex in zip(predictions, task.get("test", [])):
        total += 1
        if "output" in ex:
            if pred == ex["output"]:
                correct += 1

# ------------------------------
# Report
# ------------------------------

print("\n====================")
print(f"Total examples: {total + skipped}")
print(f"Correct: {correct}")
print(f"Skipped: {skipped}")
accuracy = (correct / total) * 100 if total else 0.0
print(f"Accuracy: {accuracy:.2f}%")
print("====================")
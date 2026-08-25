import json
import os

# ------------------------------
# Load cross_big.json
# ------------------------------
file_path = os.path.join(os.path.dirname(__file__), "cross_big.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("RUNNING CROSS CHECKER")

train = data.get("train", [])
test = data.get("test", [])

# ------------------------------
# Helpers
# ------------------------------
def same_grid(a, b):
    return a == b

def make_cross_output(val):
    return [
        [0, val, 0],
        [val, val, val],
        [0, val, 0]
    ]

def is_valid_cross_case(grid):
    top = grid[0][1]
    left = grid[1][0]
    center = grid[1][1]
    right = grid[1][2]
    bottom = grid[2][1]

    # full cross
    if center != 0 and top == center and left == center and right == center and bottom == center:
        return True

    # top-heavy
    val = grid[0][0]
    if val != 0 and grid[0][1] == val and grid[0][2] == val and center == val and bottom == val:
        return True

    # bottom-heavy
    val = grid[2][0]
    if val != 0 and grid[2][1] == val and grid[2][2] == val and center == val and top == val:
        return True

    return False

# ------------------------------
# Current solver rule
# ------------------------------
def solve_grid(grid):
    top = grid[0][1]
    left = grid[1][0]
    center = grid[1][1]
    right = grid[1][2]
    bottom = grid[2][1]

    # full cross
    if center != 0 and top == center and left == center and right == center and bottom == center:
        return make_cross_output(center)

    # top-heavy clue
    if grid[0][0] != 0 and grid[0][1] == grid[0][0] and grid[0][2] == grid[0][0] and center == grid[0][0] and bottom == grid[0][0]:
        return make_cross_output(grid[0][0])

    # bottom-heavy clue
    if grid[2][0] != 0 and grid[2][1] == grid[2][0] and grid[2][2] == grid[2][0] and center == grid[2][0] and top == grid[2][0]:
        return make_cross_output(grid[2][0])

    return None

# ------------------------------
# Check training
# ------------------------------
print(f"Training examples found: {len(train)}")
print(f"Test examples found: {len(test)}")

print("\nChecking training:")
train_pass = 0
for i, example in enumerate(train, start=1):
    pred = solve_grid(example["input"])
    ok = pred == example["output"]
    if ok:
        train_pass += 1
    print(f"Train {i}: {'PASS' if ok else 'FAIL'}")

# ------------------------------
# Check tests
# ------------------------------
total = 0
correct = 0
wrong = 0

label_stats = {}

wrong_examples = []

for i, example in enumerate(test, start=1):
    inp = example["input"]
    expected = example.get("expected_output")
    label = example.get("label", "unknown")

    pred = solve_grid(inp)

    ok = pred == expected

    total += 1
    if ok:
        correct += 1
    else:
        wrong += 1
        wrong_examples.append({
            "index": i,
            "label": label,
            "input": inp,
            "expected": expected,
            "predicted": pred
        })

    if label not in label_stats:
        label_stats[label] = {"total": 0, "correct": 0}

    label_stats[label]["total"] += 1
    if ok:
        label_stats[label]["correct"] += 1

# ------------------------------
# Report
# ------------------------------
print("\n====================")
print(f"Train passed: {train_pass}/{len(train)}")
print(f"Test correct: {correct}/{total}")
accuracy = (correct / total) * 100 if total else 0.0
print(f"Accuracy: {accuracy:.2f}%")
print("====================")

print("\nBy label:")
for label, stats in sorted(label_stats.items()):
    total_label = stats["total"]
    correct_label = stats["correct"]
    acc_label = (correct_label / total_label) * 100 if total_label else 0.0
    print(f"{label}: {correct_label}/{total_label} ({acc_label:.2f}%)")

# ------------------------------
# Show a few failures
# ------------------------------
print("\nSample failures:")
for ex in wrong_examples[:10]:
    print(f"\nTest #{ex['index']}  Label: {ex['label']}")
    print("Input:")
    for row in ex["input"]:
        print(row)

    print("Expected:")
    if ex["expected"] is None:
        print("junk")
    else:
        for row in ex["expected"]:
            print(row)

    print("Predicted:")
    if ex["predicted"] is None:
        print("junk")
    else:
        for row in ex["predicted"]:
            print(row)

# ---------------------------------
# Save Fails
# ---------------------------------
# ------------------------------
# Save all failures to file
# ------------------------------
fail_path = os.path.join(os.path.dirname(__file__), "cross_failures.txt")

with open(fail_path, "w", encoding="utf-8") as f:
    for ex in wrong_examples:
        f.write(f"Test #{ex['index']}  Label: {ex['label']}\n")

        f.write("Input:\n")
        for row in ex["input"]:
            f.write(str(row) + "\n")

        f.write("Expected:\n")
        if ex["expected"] is None:
            f.write("junk\n")
        else:
            for row in ex["expected"]:
                f.write(str(row) + "\n")

        f.write("Predicted:\n")
        if ex["predicted"] is None:
            f.write("junk\n")
        else:
            for row in ex["predicted"]:
                f.write(str(row) + "\n")

        f.write("\n" + "=" * 40 + "\n\n")

print(f"\nSaved all failures to: {fail_path}")
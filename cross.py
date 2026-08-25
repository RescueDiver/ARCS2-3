import json
import os

# ------------------------------
# Load training file
# ------------------------------
train_file = os.path.join(os.path.dirname(__file__), "cross.json")

with open(train_file, "r", encoding="utf-8") as f:
    train_data = json.load(f)

# ------------------------------
# Load test file
# ------------------------------
test_file = os.path.join(os.path.dirname(__file__), "cross_test_34.json")

with open(test_file, "r", encoding="utf-8") as f:
    test_data = json.load(f)

print("RUNNING CROSS SHAPE LEARNER")

train = train_data.get("train", [])
test = test_data.get("test", [])

# ------------------------------
# Helpers
# ------------------------------
def make_cross_output(val):
    return [
        [0, val, 0],
        [val, val, val],
        [0, val, 0]
    ]

# ------------------------------
# Solve one grid
# ------------------------------
def solve_grid(grid):
    top = grid[0][1]
    left = grid[1][0]
    center = grid[1][1]
    right = grid[1][2]
    bottom = grid[2][1]

    corners = [grid[0][0], grid[0][2], grid[2][0], grid[2][2]]
    all_vals = [grid[r][c] for r in range(3) for c in range(3)]

    # reject full same-number grid
    if all(v == all_vals[0] for v in all_vals):
        return None

    # full cross:
    # cross positions all same nonzero value
    # and not all corners also equal that value
    if center != 0 and top == center and left == center and right == center and bottom == center:
        if not all(c == center for c in corners):
            return make_cross_output(center)

    # top-heavy clue
    if grid[0][0] != 0:
        val = grid[0][0]
        if grid[0][1] == val and grid[0][2] == val and center == val and bottom == val:
            return make_cross_output(val)

    # bottom-heavy clue
    if grid[2][0] != 0:
        val = grid[2][0]
        if grid[2][1] == val and grid[2][2] == val and center == val and top == val:
            return make_cross_output(val)

    return None

# ------------------------------
# Show training check
# ------------------------------
print("\nChecking training:")
for i, example in enumerate(train, start=1):
    pred = solve_grid(example["input"])
    ok = pred == example["output"]
    print(f"Train {i}: {'PASS' if ok else 'FAIL'}")

# ------------------------------
# Run tests
# ------------------------------
print("\nTesting inputs:")
for i, example in enumerate(test, start=1):
    result = solve_grid(example["input"])

    print(f"\nTest {i}")
    print("Input:")
    for row in example["input"]:
        print(row)

    if result is None:
        print("Result: junk")
    else:
        print("Output:")
        for row in result:
            print(row)
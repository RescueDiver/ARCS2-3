import json
import os
import random

random.seed(1)

def make_cross_output(val):
    return [
        [0, val, 0],
        [val, val, val],
        [0, val, 0]
    ]

def make_vertical_junk(val, fillers):
    return [
        [fillers[0], val, fillers[1]],
        [fillers[2], val, fillers[3]],
        [fillers[4], val, fillers[5]]
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
# Training set (same as before)
# ------------------------------
train = [
    {
        "input": [
            [0, 2, 0],
            [2, 2, 2],
            [0, 2, 0]
        ],
        "output": [
            [0, 2, 0],
            [2, 2, 2],
            [0, 2, 0]
        ]
    },
    {
        "input": [
            [2, 2, 2],
            [0, 2, 0],
            [0, 2, 0]
        ],
        "output": [
            [0, 2, 0],
            [2, 2, 2],
            [0, 2, 0]
        ]
    },
    {
        "input": [
            [0, 2, 0],
            [0, 2, 0],
            [2, 2, 2]
        ],
        "output": [
            [0, 2, 0],
            [2, 2, 2],
            [0, 2, 0]
        ]
    }
]

# ------------------------------
# Build test set
# ------------------------------
tests = []

for val in range(1, 10):
    made = 0
    while made < 200:
        fillers = [random.randint(0, 9) for _ in range(6)]
        grid = make_vertical_junk(val, fillers)

        # skip if accidentally valid
        if is_valid_cross_case(grid):
            continue

        tests.append({
            "input": grid,
            "expected_output": None,
            "label": "junk_vertical"
        })
        made += 1

# ------------------------------
# Save JSON
# ------------------------------
data = {
    "train": train,
    "test": tests
}

file_path = os.path.join(os.path.dirname(__file__), "cross_big.json")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Saved {len(tests)} clean test cases")
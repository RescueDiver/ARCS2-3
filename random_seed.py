import json
import os
import random

random.seed(1)

# ------------------------------
# Base output builder
# ------------------------------
def make_cross_output(val):
    return [
        [0, val, 0],
        [val, val, val],
        [0, val, 0]
    ]

# ------------------------------
# Valid pattern builders
# ------------------------------
def make_full_cross_input(val, corners):
    return [
        [corners[0], val, corners[1]],
        [val, val, val],
        [corners[2], val, corners[3]]
    ]

def make_top_heavy_input(val, fillers):
    return [
        [val, val, val],
        [fillers[0], val, fillers[1]],
        [fillers[2], val, fillers[3]]
    ]

def make_bottom_heavy_input(val, fillers):
    return [
        [fillers[0], val, fillers[1]],
        [fillers[2], val, fillers[3]],
        [val, val, val]
    ]

# ------------------------------
# Junk pattern builders
# ------------------------------
def make_vertical_junk(val, fillers):
    return [
        [fillers[0], val, fillers[1]],
        [fillers[2], val, fillers[3]],
        [fillers[4], val, fillers[5]]
    ]

def make_x_junk(val, fillers):
    return [
        [val, fillers[0], val],
        [fillers[1], val, fillers[2]],
        [val, fillers[3], val]
    ]

def make_mixed_cross_junk(a, b, fillers):
    return [
        [fillers[0], a, fillers[1]],
        [a, b, a],
        [fillers[2], a, fillers[3]]
    ]

def make_same_number_grid(val):
    return [
        [val, val, val],
        [val, val, val],
        [val, val, val]
    ]

# ------------------------------
# Training set
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
# Build large test set
# expected_output = null means junk
# ------------------------------
tests = []

# valid full cross cases
for val in range(1, 10):
    for _ in range(40):
        corners = [random.randint(0, 9) for _ in range(4)]
        tests.append({
            "input": make_full_cross_input(val, corners),
            "expected_output": make_cross_output(val),
            "label": "valid_full_cross"
        })

# valid top-heavy cases
for val in range(1, 10):
    for _ in range(30):
        fillers = [random.randint(0, 9) for _ in range(4)]
        tests.append({
            "input": make_top_heavy_input(val, fillers),
            "expected_output": make_cross_output(val),
            "label": "valid_top_heavy"
        })

# valid bottom-heavy cases
for val in range(1, 10):
    for _ in range(30):
        fillers = [random.randint(0, 9) for _ in range(4)]
        tests.append({
            "input": make_bottom_heavy_input(val, fillers),
            "expected_output": make_cross_output(val),
            "label": "valid_bottom_heavy"
        })

# junk vertical-line cases
for val in range(1, 10):
    for _ in range(20):
        fillers = [random.randint(0, 9) for _ in range(6)]
        tests.append({
            "input": make_vertical_junk(val, fillers),
            "expected_output": None,
            "label": "junk_vertical"
        })

# junk x-shape cases
for val in range(1, 10):
    for _ in range(20):
        fillers = [random.randint(0, 9) for _ in range(4)]
        tests.append({
            "input": make_x_junk(val, fillers),
            "expected_output": None,
            "label": "junk_x"
        })

# junk mixed-cross cases
for a in range(1, 10):
    for b in range(1, 10):
        if a == b:
            continue
        for _ in range(6):
            fillers = [random.randint(0, 9) for _ in range(4)]
            tests.append({
                "input": make_mixed_cross_junk(a, b, fillers),
                "expected_output": None,
                "label": "junk_mixed_cross"
            })

# junk same-number full grids
for val in range(1, 10):
    tests.append({
        "input": make_same_number_grid(val),
        "expected_output": None,
        "label": "junk_same_number_grid"
    })

# shuffle so test order is mixed
random.shuffle(tests)

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

print(f"Saved {len(tests)} test cases to cross_big.json")
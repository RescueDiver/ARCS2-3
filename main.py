import json
import os
from copy import deepcopy
from collections import Counter

# =============================
# LOAD DATASET
# =============================
file_path = os.path.join(os.path.dirname(__file__), "data.json")

with open(file_path, "r", encoding="utf-8") as f:
    dataset = json.load(f)

tasks = list(dataset.values())
task_ids = list(dataset.keys())

print(f"Loaded dataset with {len(tasks)} tasks.\n")


# =============================
# HELPER FUNCTIONS
# =============================
def grids_equal(g1, g2):
    return g1 == g2


def get_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    vals = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                vals.append(grid[nr][nc])
    return vals


# =============================
# RULES
# =============================

# Rule 1: Majority neighbor
def rule_majority(grid):
    rows, cols = len(grid), len(grid[0])
    result = deepcopy(grid)

    for r in range(rows):
        for c in range(cols):
            neighbors = get_neighbors(grid, r, c)
            if neighbors:
                result[r][c] = Counter(neighbors).most_common(1)[0][0]

    return result


# Rule 2: Fill zeros
def rule_fill_zero(grid):
    rows, cols = len(grid), len(grid[0])
    result = deepcopy(grid)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                neighbors = get_neighbors(grid, r, c)
                non_zero = [v for v in neighbors if v != 0]
                if non_zero:
                    result[r][c] = Counter(non_zero).most_common(1)[0][0]

    return result


# Rule 3: Expand colors
def rule_expand(grid):
    rows, cols = len(grid), len(grid[0])
    result = deepcopy(grid)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if result[nr][nc] == 0:
                                result[nr][nc] = grid[r][c]

    return result


# Rule 4: Identity
def rule_identity(grid):
    return deepcopy(grid)


# Rule 5: Flip horizontal
def rule_flip_horizontal(grid):
    return [row[::-1] for row in grid]


# Rule 6: Flip vertical
def rule_flip_vertical(grid):
    return grid[::-1]


# Rule 7: Rotate 90°
def rule_rotate_90(grid):
    return [list(row) for row in zip(*grid[::-1])]


# Rule 8: Color mapping (simple)
def rule_color_map(grid):
    flat = [v for row in grid for v in row]
    counts = Counter(flat)

    if not counts:
        return grid

    most_common = counts.most_common()
    dominant = most_common[0][0]

    mapping = {color: dominant for color, _ in most_common}

    return [[mapping[v] for v in row] for row in grid]


# =============================
# RULE SET
# =============================
RULES = [
    ("identity", rule_identity),
    ("majority", rule_majority),
    ("fill_zero", rule_fill_zero),
    ("expand", rule_expand),
    ("flip_h", rule_flip_horizontal),
    ("flip_v", rule_flip_vertical),
    ("rotate_90", rule_rotate_90),
    ("color_map", rule_color_map),
]


# =============================
# FIND BEST RULE
# =============================
def find_best_rule(train_pairs):
    best_rules = []
    best_score = -1

    for name, rule in RULES:
        score = 0

        for pair in train_pairs:
            inp = pair["input"]
            expected = pair["output"]

            pred = rule(inp)

            if grids_equal(pred, expected):
                score += 1

        if score > best_score:
            best_score = score
            best_rules = [(name, rule)]
        elif score == best_score:
            best_rules.append((name, rule))

    # If nothing worked → skip task
    if best_score == 0:
        return None

    return best_rules[0]


# =============================
# TEST HARNESS
# =============================
total = 0
correct = 0
skipped = 0

for i, task in enumerate(tasks):
    task_id = task_ids[i]

    train = task.get("train", [])
    test = task.get("test", [])

    if not train or not test:
        continue

    best = find_best_rule(train)

    if best is None:
        print(f"Task {task_id} → no matching rule (skipped)")
        skipped += len(test)
        continue

    rule_name, rule_fn = best

    print(f"Task {task_id} → using rule: {rule_name}")

    for pair in test:
        inp = pair["input"]
        expected = pair.get("output")

        pred = rule_fn(inp)

        total += 1

        if expected is not None and grids_equal(pred, expected):
            correct += 1


# =============================
# RESULTS
# =============================
print("\n====================")
print(f"Total examples: {total}")
print(f"Correct: {correct}")
print(f"Skipped: {skipped}")
if total > 0:
    print(f"Accuracy: {correct/total*100:.2f}%")
print("====================")
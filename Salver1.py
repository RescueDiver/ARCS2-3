import json
import os

# ------------------------------
# Load data
# ------------------------------
file_path = os.path.join(os.path.dirname(__file__), "small.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("RUNNING REAL SOLVER")

train = data["train"]
test = data["test"]

# ------------------------------
# Solve grid using correct rule
# ------------------------------
def solve_grid(grid):
    h = len(grid)
    w = len(grid[0])

    # collect all nonzero points
    points = []
    for r in range(h):
        for c in range(w):
            if grid[r][c] != 0:
                points.append((r, c, grid[r][c]))

    out = [[0 for _ in range(w)] for _ in range(h)]

    for r in range(h):
        for c in range(w):
            best_dist = None
            best_color = 0

            for pr, pc, color in points:
                # only same row or column matters
                if pr == r or pc == c:
                    dist = abs(pr - r) + abs(pc - c)

                    if best_dist is None or dist < best_dist:
                        best_dist = dist
                        best_color = color

            out[r][c] = best_color

    return out

# ------------------------------
# Check training (VERY IMPORTANT)
# ------------------------------
print("\nChecking training:")

all_ok = True
for i, ex in enumerate(train):
    pred = solve_grid(ex["input"])
    ok = pred == ex["output"]
    print(f"Train {i+1}: {'PASS' if ok else 'FAIL'}")
    if not ok:
        all_ok = False

# ------------------------------
# Solve first 3 test problems
# ------------------------------
print("\nGenerated outputs:")

for i in range(3):
    result = solve_grid(test[i]["input"])

    print(f"\nProblem {i+1}")
    for row in result:
        print(row)

print("\nTraining match:", all_ok)
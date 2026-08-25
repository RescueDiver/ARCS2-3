import json
import os
import numpy as np


def solve_logic(input_grid):
    """
    Core Logic: Measure the yellow marker (4) at the bottom.
    If an azure (8) row span matches that width, fill Yellow (4).
    Otherwise, fill Green (3).
    """
    grid = np.array(input_grid)
    output_grid = np.copy(grid)

    # Find all yellow pixels
    yellow_coords = np.argwhere(grid == 4)
    if yellow_coords.size == 0:
        return grid.tolist()

    # Get width of the reference marker (usually the bottom-most one)
    marker_width = yellow_coords[:, 1].max() - yellow_coords[:, 1].min() + 1

    for r in range(grid.shape[0]):
        azure_pixels = np.where(grid[r, :] == 8)[0]
        if len(azure_pixels) >= 2:
            start, end = azure_pixels.min(), azure_pixels.max()
            span = end - start + 1

            # Apply conditional color
            fill_color = 4 if span == marker_width else 3
            output_grid[r, start:end + 1] = fill_color

    return output_grid.tolist()


def run_project():
    base_dir = os.path.join(os.path.expanduser("~"), "Desktop", "ARC_Puzzles")
    input_file = os.path.join(base_dir, "task.json")
    output_file = os.path.join(base_dir, "task_solved.json")

    if not os.path.exists(input_file):
        print(f"❌ ERROR: File not found at {input_file}")
        return

    try:
        with open(input_file, 'r') as f:
            data = json.load(f)

        # This dictionary will hold our results
        solved_output = {}

        # 1. Check if the JSON is a simple "input/output" pair
        if "input" in data:
            solved_output["input"] = data["input"]
            solved_output["output"] = solve_logic(data["input"])

        # 2. Check if it's a nested task (like "221dfab4": {"train": [...]})
        else:
            for task_id, task_content in data.items():
                if isinstance(task_content, dict):
                    solved_output[task_id] = {"train": [], "test": []}
                    for mode in ["train", "test"]:
                        if mode in task_content:
                            for item in task_content[mode]:
                                solved_output[task_id][mode].append({
                                    "input": item["input"],
                                    "output": solve_logic(item["input"])
                                })
                else:
                    # If it's just a raw list/grid
                    solved_output["output"] = solve_logic(data)

        # 3. Save the Results
        with open(output_file, 'w') as f:
            json.dump(solved_output, f, indent=4)

        print(f"✅ SUCCESS: Processed and saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    run_project()
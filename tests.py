import json
import os

file_path = os.path.join(os.path.dirname(__file__), "data.json")

# Load dataset ONCE
with open(file_path, "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Convert dict → list
tasks = list(dataset.values())
task_ids = list(dataset.keys())

print(f"Loaded dataset with {len(tasks)} tasks.\n")

# Show first 5
for i, task in enumerate(tasks[:5]):
    print(f"Task {i+1} ID: {task_ids[i]}")

print(f"Loaded dataset with {len(dataset)} tasks.")

# Example: iterate tasks safely
for task in dataset:
    if isinstance(task, dict):
        task_id = task.get("task_id", "unknown")
        print(f"Task ID: {task_id}")
    else:
        print("Skipping invalid task:", task)
import sys
import json
import os
from datetime import datetime

# Configuration
DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def generate_id(tasks):
    return max([t['id'] for t in tasks], default=0) + 1

def add_task(description):
    tasks = load_tasks()
    new_task = {
        "id": generate_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")

def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == int(task_id):
            task['description'] = description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print("Task updated successfully")
            return
    print("Error: Task ID not found")

def delete_task(task_id):
    tasks = load_tasks()
    updated_tasks = [t for t in tasks if t['id'] != int(task_id)]
    if len(tasks) == len(updated_tasks):
        print("Error: Task ID not found")
    else:
        save_tasks(updated_tasks)
        print("Task deleted successfully")

def change_status(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == int(task_id):
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task marked as {status}")
            return
    print("Error: Task ID not found")

def list_tasks(filter_status=None):
    tasks = load_tasks()
    filtered = [t for t in tasks if filter_status is None or t['status'] == filter_status]
    
    if not filtered:
        print("No tasks found.")
        return

    print(f"{'ID':<5} | {'Status':<12} | {'Description'}")
    print("-" * 40)
    for t in filtered:
        print(f"{t['id']:<5} | {t['status']:<12} | {t['description']}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python task_cli.py [command] [args]")
        return

    cmd = sys.argv[1]

    try:
        if cmd == "add" and len(sys.argv) > 2:
            add_task(sys.argv[2])
        elif cmd == "update" and len(sys.argv) > 3:
            update_task(sys.argv[2], sys.argv[3])
        elif cmd == "delete" and len(sys.argv) > 2:
            delete_task(sys.argv[2])
        elif cmd == "mark-in-progress" and len(sys.argv) > 2:
            change_status(sys.argv[2], "in-progress")
        elif cmd == "mark-done" and len(sys.argv) > 2:
            change_status(sys.argv[2], "done")
        elif cmd == "list":
            status_map = {"todo": "todo", "done": "done", "in-progress": "in-progress"}
            filter_val = status_map.get(sys.argv[2]) if len(sys.argv) > 2 else None
            list_tasks(filter_val)
        else:
            print("Unknown command or missing arguments.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

import os

TASKS_FILE = "tasks.txt"
COMPLETED_FILE = "completed_tasks.txt"

def add_task(task):
    with open(TASKS_FILE, "a") as f:
        f.write(task + "\n")
    print(f"Task added: {task}")

def list_tasks():
    if not os.path.exists(TASKS_FILE):
        print("No tasks found.")
        return
    with open(TASKS_FILE, "r") as f:
        tasks = f.readlines()
    if tasks:
        print("Tasks:")
        for idx, task in enumerate(tasks, start=1):
            print(f"{idx}. {task.strip()}")
    else:
        print("No tasks available.")

def complete_task(task_number):
    if not os.path.exists(TASKS_FILE):
        print("No tasks found.")
        return
    with open(TASKS_FILE, "r") as f:
        tasks = f.readlines()

    if task_number < 1 or task_number > len(tasks):
        print("Invalid task number.")
        return

    completed_task = tasks.pop(task_number - 1).strip()
    
    with open(TASKS_FILE, "w") as f:
        f.writelines(tasks)
    
    with open(COMPLETED_FILE, "a") as f:
        f.write(completed_task + "\n")

    print(f"Task completed: {completed_task}")

if __name__ == "__main__":
    while True:
        command = input("Enter command (add/list/done/exit): ").strip().lower()
        if command == "add":
            task = input("Enter task: ").strip()
            add_task(task)
        elif command == "list":
            list_tasks()
        elif command == "done":
            task_number = int(input("Enter task number to mark as done: "))
            complete_task(task_number)
        elif command == "exit":
            break
        else:
            print("Invalid command.")

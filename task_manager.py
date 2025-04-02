import sqlite3
import sys
import datetime

DB_NAME = "taskList.db"

def create_connection():
    """Establish a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)

def create_tables():
    """Create necessary tables if they do not exist."""
    with create_connection() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        status TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS task_history (
                        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task_id INTEGER,
                        change_type TEXT NOT NULL,
                        change_description TEXT,
                        change_timestamp TEXT NOT NULL,
                        FOREIGN KEY (task_id) REFERENCES tasks(id)
                    )''')
        conn.commit()

def add_task(title, description):
    """Add a new task to the database."""
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = "incomplete"
    
    with create_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO tasks (title, description, status, created_at) VALUES (?, ?, ?, ?)",
                  (title, description, status, created_at))
        task_id = c.lastrowid
        c.execute("INSERT INTO task_history (task_id, change_type, change_description, change_timestamp) VALUES (?, ?, ?, ?)",
                  (task_id, "created", f"Task '{title}' was created.", created_at))
        conn.commit()
    print("✔ Task added successfully!")

def view_tasks():
    """Display all tasks."""
    with create_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks")
        tasks = c.fetchall()
    
    if not tasks:
        print("No tasks found.")
    else:
        print_table(tasks, ["ID", "Title", "Description", "Status", "Created At", "Updated At"])

def edit_task(task_id, new_title, new_description):
    """Edit an existing task."""
    updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with create_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT title FROM tasks WHERE id=?", (task_id,))
        task = c.fetchone()
        if not task:
            print("❌ Task not found.")
            return
        
        c.execute("UPDATE tasks SET title=?, description=?, updated_at=? WHERE id=?",
                  (new_title, new_description, updated_at, task_id))
        c.execute("INSERT INTO task_history (task_id, change_type, change_description, change_timestamp) VALUES (?, ?, ?, ?)",
                  (task_id, "updated", f"Task '{task[0]}' was updated.", updated_at))
        conn.commit()
    print("✔ Task updated successfully!")

def view_task_history(task_id):
    """View the history of a specific task."""
    with create_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM task_history WHERE task_id=?", (task_id,))
        histories = c.fetchall()

    if not histories:
        print("No history found for this task.")
    else:
        print_table(histories, ["History ID", "Task ID", "Change Type", "Change Description", "Change Timestamp"])


def complete_task(task_id):
    """Mark a task as completed."""
    completed_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with create_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT title FROM tasks WHERE id=?", (task_id,))
        task = c.fetchone()
        if not task:
            print("❌ Task not found.")
            return
        
        c.execute("UPDATE tasks SET status='completed', updated_at=? WHERE id=?", (completed_at, task_id))
        c.execute("INSERT INTO task_history (task_id, change_type, change_description, change_timestamp) VALUES (?, ?, ?, ?)",
                  (task_id, "completed", f"Task '{task[0]}' marked as completed.", completed_at))
        conn.commit()
    print("✔ Task marked as completed!")

def delete_task(task_id):
    """Delete a task and its history."""
    with create_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT title FROM tasks WHERE id=?", (task_id,))
        task = c.fetchone()
        if not task:
            print("❌ Task not found.")
            return
        
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        c.execute("DELETE FROM task_history WHERE task_id=?", (task_id,))
        conn.commit()
    print("✔ Task deleted successfully!")

def print_table(data, headers):
    """Prints data in a table format."""
    if not data:
        print("No records found.")
        return

    # Convert None values to empty strings
    formatted_data = [
        tuple("" if item is None else item for item in row) for row in data
    ]

    col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *formatted_data)]
    format_str = " | ".join("{:<" + str(width) + "}" for width in col_widths)

    print(format_str.format(*headers))
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))

    for row in formatted_data:
        print(format_str.format(*row))


def main():
    create_tables()
    print("Welcome to the Task Management Tool! 🚀")
    
    while True:
        print("\nOptions:")
        print("1.Add Task")
        print("2.Edit Task")
        print("3.Complete Task")
        print("4.View Tasks")
        print("5.View Task History")
        print("6.Delete Task")
        print("7.Exit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            add_task(title, description)
        elif choice == "2":
            task_id = int(input("Enter task ID: "))
            new_title = input("New title: ")
            new_description = input("New description: ")
            edit_task(task_id, new_title, new_description)
        elif choice == "3":
            task_id = int(input("Enter task ID: "))
            complete_task(task_id)
        elif choice == "4":
            view_tasks()
        elif choice == "5":
            task_id = int(input("Enter task ID to view history: "))
            view_task_history(task_id)
        elif choice == "6":
            task_id = int(input("Enter task ID: "))
            delete_task(task_id)
        elif choice == "7":
            print("👋 Exiting Task Manager.")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Try again!")

if __name__ == "__main__":
    main()

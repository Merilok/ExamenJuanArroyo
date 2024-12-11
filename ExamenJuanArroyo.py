import heapq
import json
import os

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.heap = []  # Priority queue
        self.tasks = {}  # To track tasks by name
        self.filename = filename
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from a file."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)
                for task in data:
                    self.add_task(task["name"], task["priority"], task["dependencies"], persist=False)

    def save_tasks(self):
        """Save tasks to a file."""
        with open(self.filename, "w") as file:
            tasks = [{"name": name, "priority": priority, "dependencies": dependencies}
                     for priority, name, dependencies in self.heap]
            json.dump(tasks, file, indent=4)

    def add_task(self, name, priority, dependencies=None, persist=True):
        """Add a new task."""
        if not name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(priority, int):
            raise ValueError("Priority must be an integer.")

        dependencies = dependencies or []

        if name in self.tasks:
            raise ValueError("Task with this name already exists.")

        heapq.heappush(self.heap, (priority, name, dependencies))
        self.tasks[name] = (priority, dependencies)

        if persist:
            self.save_tasks()

    def show_tasks(self):
        """Display all tasks ordered by priority."""
        for priority, name, dependencies in sorted(self.heap):
            print(f"Priority: {priority}, Name: {name}, Dependencies: {dependencies}")

    def complete_task(self, name):
        """Mark a task as completed."""
        if name not in self.tasks:
            raise ValueError("Task not found.")

        self.heap = [(priority, task_name, dependencies) for priority, task_name, dependencies in self.heap if task_name != name]
        heapq.heapify(self.heap)
        del self.tasks[name]

        self.save_tasks()

    def next_task(self):
        """Get the next task of highest priority without removing it."""
        if not self.heap:
            return None
        priority, name, dependencies = self.heap[0]
        return {"name": name, "priority": priority, "dependencies": dependencies}

# Example usage
if __name__ == "__main__":
    manager = TaskManager()


   


    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. Show Tasks")
        print("3. Complete Task")
        print("4. Next Task")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Task name: ")
            try:
                priority = int(input("Priority (lower number = higher priority): "))
                dependencies = input("Dependencies (comma-separated): ").split(",")
                dependencies = [dep.strip() for dep in dependencies if dep.strip()]
                manager.add_task(name, priority, dependencies)
                print("Task added successfully.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "2":
            manager.show_tasks()
        elif choice == "3":
            name = input("Task name to complete: ")
            try:
                manager.complete_task(name)
                print("Task completed successfully.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "4":
            task = manager.next_task()
            if task:
                print(f"Next Task: {task}")
            else:
                print("No tasks available.")
        elif choice == "5":
            break
        else:
            print("Invalid option. Please try again.")

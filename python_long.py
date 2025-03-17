import random
import logging
import argparse
import sys
import os
from datetime import datetime
from functools import wraps
from typing import List, Iterator, Callable

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def measure_time(func: Callable) -> Callable:
    """
    Decorator to measure and log the execution time of a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        logging.debug(f"Starting '{func.__name__}'")
        result = func(*args, **kwargs)
        duration = (datetime.now() - start_time).total_seconds()
        logging.debug(f"Finished '{func.__name__}' in {duration:.4f} seconds")
        return result
    return wrapper

class Task:
    """
    Represents a single to-do item.
    """
    def __init__(self, task_id: int, description: str, completed: bool = False) -> None:
        self.task_id = task_id
        self.description = description
        self.completed = completed

    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def __str__(self) -> str:
        status = "Done" if self.completed else "Pending"
        return f"Task {self.task_id}: {self.description} [{status}]"

class TodoList:
    """
    Manages a list of tasks, with functionality to add, remove, and update tasks.
    """
    def __init__(self) -> None:
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, description: str) -> None:
        """Add a new task with a given description."""
        task = Task(task_id=self.next_id, description=description)
        self.tasks.append(task)
        logging.info(f"Added {task}")
        self.next_id += 1

    def remove_task(self, task_id: int) -> bool:
        """Remove a task by its ID; return True if removed, False if not found."""
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                logging.info(f"Removed Task {task_id}")
                return True
        logging.warning(f"Task {task_id} not found for removal")
        return False

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed by its ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                task.mark_completed()
                logging.info(f"Completed {task}")
                return True
        logging.warning(f"Task {task_id} not found for completion")
        return False

    def list_tasks(self) -> None:
        """Print all tasks in the to-do list."""
        if not self.tasks:
            print("No tasks available.")
        else:
            for task in self.tasks:
                print(task)

    def tasks_generator(self) -> Iterator[Task]:
        """
        A generator to yield tasks one by one.
        Demonstrates use of generator functions.
        """
        for task in self.tasks:
            yield task

    def get_pending_tasks(self) -> List[Task]:
        """Return a list of pending tasks using a list comprehension."""
        return [task for task in self.tasks if not task.completed]

@measure_time
def process_tasks(todo: TodoList) -> None:
    """
    Process tasks in the TodoList.
    Demonstrates iteration, exception handling, lambda functions, and filtering.
    """
    try:
        # Use a lambda to filter tasks with a description length shorter than 10 characters
        short_tasks = list(filter(lambda t: len(t.description) < 10, todo.tasks))
        logging.info(f"Found {len(short_tasks)} tasks with a short description")
        # Iterate through tasks via generator and complete those marked as 'urgent'
        for task in todo.tasks_generator():
            if "urgent" in task.description.lower():
                todo.complete_task(task.task_id)
    except Exception as e:
        logging.error(f"Error processing tasks: {e}")

def save_tasks_to_file(todo: TodoList, filename: str) -> None:
    """
    Save all tasks to a file.
    Demonstrates file I/O and use of context managers.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for task in todo.tasks:
                file.write(f"{task.task_id},{task.description},{task.completed}\n")
        logging.info(f"Tasks saved to {filename}")
    except IOError as e:
        logging.error(f"Error writing to file {filename}: {e}")

def load_tasks_from_file(todo: TodoList, filename: str) -> None:
    """
    Load tasks from a file and add them to the TodoList.
    Uses a context manager to safely open the file.
    """
    if not os.path.exists(filename):
        logging.warning(f"File {filename} not found. Skipping load.")
        return
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    task_id, description, completed_str = parts
                    task = Task(task_id=int(task_id), description=description, completed=(completed_str == "True"))
                    todo.tasks.append(task)
                    todo.next_id = max(todo.next_id, task.task_id + 1)
        logging.info(f"Loaded tasks from {filename}")
    except Exception as e:
        logging.error(f"Error loading tasks from {filename}: {e}")

def additional_demo_features() -> None:
    """
    Demonstrates additional Python features including comprehensions,
    nested functions, and exception handling.
    """
    # List and dictionary comprehensions
    numbers = [i for i in range(10)]
    squares = {i: i * i for i in numbers}
    print("Numbers:", numbers)
    print("Squares:", squares)

    # Nested function with closure
    def outer(message: str):
        def inner():
            print(f"Inner says: {message}")
        return inner
    greeting = outer("Hello from the nested function!")
    greeting()

    # Demonstrate exception handling with a try/except block
    try:
        result = 10 / random.choice([0, 2, 5])
        print("Result:", result)
    except ZeroDivisionError:
        print("Caught division by zero error!")

def main():
    parser = argparse.ArgumentParser(description="Todo List Application Example")
    parser.add_argument("--file", type=str, default="tasks.txt", help="Filename to load/save tasks")
    parser.add_argument("--add", type=str, help="Add a new task with the given description")
    parser.add_argument("--complete", type=int, help="Mark a task as completed by task ID")
    parser.add_argument("--remove", type=int, help="Remove a task by task ID")
    parser.add_argument("--list", action="store_true", help="List all tasks")
    parser.add_argument("--demo", action="store_true", help="Run additional demo features")
    args = parser.parse_args()

    todo = TodoList()
    load_tasks_from_file(todo, args.file)

    if args.add:
        todo.add_task(args.add)
    if args.complete:
        todo.complete_task(args.complete)
    if args.remove:
        todo.remove_task(args.remove)
    if args.list:
        todo.list_tasks()

    # Process tasks with performance measurement
    process_tasks(todo)
    save_tasks_to_file(todo, args.file)

    if args.demo:
        additional_demo_features()

if __name__ == "__main__":
    main()

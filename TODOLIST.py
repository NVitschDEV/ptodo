import json
import os
import time

from rich import print as rprint
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

FILENAME = "TODOLIST.json"
console = Console()


def load_todos():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            data = json.load(f)
            # Migration: if the file has old strings, convert them to dictionaries
            if data and isinstance(data[0], str):
                return [{"task": t, "done": False} for t in data]
            return data
    return []


def save_todos(todos):
    with open(FILENAME, "w") as f:
        json.dump(todos, f, indent=4)


def get_task_table(todos):
    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("#", style="dim", width=4, justify="center")
    table.add_column("Task", style="cyan")
    table.add_column("Status", justify="right")

    if not todos:
        return Panel("No tasks found! Get to work!", style="red")

    for idx, item in enumerate(todos, 1):
        # Check if done to change display
        task_text = item["task"]
        if item["done"]:
            status = "[bold green]✔ Done[/bold green]"
            display_task = f"[strike dim]{task_text}[/strike dim]"
        else:
            status = "[yellow]Pending[/yellow]"
            display_task = task_text

        table.add_row(str(idx), display_task, status)

    return table


def print_header():
    os.system("cls" if os.name == "nt" else "clear")
    logo = """
    [bold red]___________________  ________    ________  .____    .___  ____________________[/bold red]
    [bold red]\__    ___/\_____  \ \______ \   \_____  \ |    |   |   |/     _____/\__    ___/[/bold red]
    [bold blue1]  |    |    /   |   \ |    |  \   /   |   \|    |   |   |\_____  \     |    |[/bold blue1]
    [bold blue]  |    |   /    |    \|    `   \ /    |    \    |___|   |/        \    |    |[/bold blue]
    [bold blue]  |____|   \_______  /_______  / \_______  /_______ \___/_______  /    |____|[/bold blue]
    [dim]                   \/        \/          \/        \/           \/[/dim]
    """
    console.print(Align.center(logo))


def add_mode(todos):
    while True:
        print_header()
        console.print(get_task_table(todos))
        task = Prompt.ask("\n[bold green]Add Task[/bold green] (or 'exit')")
        if task.lower() == "exit":
            break
        # Save as a dictionary now
        todos.append({"task": task, "done": False})
        save_todos(todos)
        console.print(f"[green]Added:[/green] {task}")
        time.sleep(0.5)


def complete_mode(todos):
    while True:
        print_header()
        console.print(get_task_table(todos))
        task_num = Prompt.ask("\n[bold green]Complete Number[/bold green] (or 'exit')")
        if task_num.lower() == "exit":
            break
        if task_num.isdigit():
            idx = int(task_num) - 1
            if 0 <= idx < len(todos):
                todos[idx]["done"] = True
                save_todos(todos)
                console.print(f"[green]Task marked as done![/green]")
                time.sleep(1)
            else:
                console.print("[red]Invalid number![/red]")
                time.sleep(1)


def remove_mode(todos):
    while True:
        print_header()
        console.print(get_task_table(todos))
        task_num = Prompt.ask("\n[bold red]Delete Number[/bold red] (or 'exit')")
        if task_num.lower() == "exit":
            break
        if task_num.isdigit():
            idx = int(task_num) - 1
            if 0 <= idx < len(todos):
                removed = todos.pop(idx)["task"]
                save_todos(todos)
                console.print(f"[red]Removed:[/red] {removed}")
                time.sleep(1)
            else:
                console.print("[red]Invalid number![/red]")
                time.sleep(1)


def app():
    todos = load_todos()
    while True:
        print_header()
        console.print(
            Panel(
                get_task_table(todos), title="Current To-Do List", border_style="blue"
            )
        )

        console.print("\n[1] [bold green]Add Task[/bold green]")
        console.print("[2] [bold blue1]Complete Task[/bold blue1]")
        console.print("[3] [bold red]Remove Task[/bold red]")
        console.print("[4] [bold white]Exit[/bold white]")

        choice = Prompt.ask("\nChoose", choices=["1", "2", "3", "4", "Exit", "exit"])

        if choice == "1":
            add_mode(todos)
        elif choice == "2":
            complete_mode(todos)
        elif choice == "3":
            remove_mode(todos)
        elif choice == "4":
            console.print("[bold yellow]Goodbye![/bold yellow]")
            break
        elif choice == "exit":
            console.print("[bold yellow]Goodbye![/bold yellow]")
            break
        elif choice == "Exit":
            console.print("[bold yellow]Goodbye![/bold yellow]")
            break  
            

app()

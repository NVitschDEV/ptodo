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
            return json.load(f)
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

    for idx, task in enumerate(todos, 1):
        table.add_row(str(idx), task, "[green]Pending[/green]")

    return table


def print_header():
    os.system("cls" if os.name == "nt" else "clear")
    logo = """
    [bold red]___________________  ________    ________  .____     .___  ____________________[/bold red]
    [bold red]\__    ___/\_____  \ \______ \   \_____  \ |    |    |   |/     _____/\__    ___/[/bold red]
    [bold blue1]  |    |    /   |   \ |    |  \   /   |   \|    |    |   |\_____  \   |    |[/bold blue1]
    [bold blue]  |    |   /    |    \|    `   \ /    |    \    |___ |   |/        \  |    |[/bold blue]
    [bold blue]  |____|   \_______  /_______  / \_______  /_______ \___/_______  /  |____|[/bold blue]
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

        todos.append(task)
        save_todos(todos)
        console.print(f"[green]Added:[/green] {task}")
        time.sleep(0.5)


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
                removed = todos.pop(idx)
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
        console.print("[2] [bold red]Remove Task[/bold red]")
        console.print("[3] [bold white]Exit[/bold white]")

        choice = Prompt.ask("\nChoose", choices=["1", "2", "3"])

        if choice == "1":
            add_mode(todos)
        elif choice == "2":
            remove_mode(todos)
        elif choice == "3":
            console.print("[bold yellow]Goodbye![/bold yellow]")
            break


app()

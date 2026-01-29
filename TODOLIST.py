import os
import pickle

# Hi

logo = r"""
___________________  ________   ________  .____    .___  ____________________
\__    ___/\_____  \ \______ \  \_____  \ |    |   |   |/   _____/\__    ___/
  |    |    /   |   \ |    |  \  /   |   \|    |   |   |\_____  \   |    |
  |    |   /    |    \|    `   \/    |    \    |___|   |/        \  |    |
  |____|   \_______  /_______  /\_______  /_______ \___/_______  /  |____|
                   \/        \/         \/        \/           \/
"""
print(logo)


def menu():
    print(r"""
    ╔══════════════════════════════════════════╗
    ║       WHAT WOULD YOU LIKE TO DO?         ║
    ╠══════════════════════════════════════════╣
    ║     [1] ADD    [2] REMOVE   [3] SHOW     ║
    ╚══════════════════════════════════════════╝
    """)


FILENAME = "hansimglück.pkl"

# Load todos
if os.path.exists(FILENAME):
    with open(FILENAME, "rb") as f:
        todos = pickle.load(f)
else:
    todos = []


def show_todo():
    for i in todos:
        print(i)


def add_task():
    hans = 1
    print("Add your Task here, write exit to exit!")
    while hans == 1:
        task = input("")
        if task == "exit":
            break
        else:
            todos.append(task)


def remove_task():
    show_todo()
    print("--------------------------")
    while 1 == 1:
        task_remove = input("")
        if task_remove in todos:
            todos.remove(task_remove)
        elif task_remove == "exit":
            break
        else:
            print("This is not a valid input")


def app():
    while 1 == 1:
        menu()
        s1 = input("")
        if s1 == "1":
            add_task()
        elif s1 == "2":
            remove_task()
        elif s1 == "3":
            show_todo()
        elif s1 == "exit":
            break
        else:
            print("This input is unvalid please try again")


app()

# Save todos
with open(FILENAME, "wb") as f:
    pickle.dump(todos, f)

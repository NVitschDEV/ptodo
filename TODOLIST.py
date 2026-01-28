import os
import pickle

logo = r"""
___________________  ________   ________  .____    .___  ____________________
\__    ___/\_____  \ \______ \  \_____  \ |    |   |   |/   _____/\__    ___/
  |    |    /   |   \ |    |  \  /   |   \|    |   |   |\_____  \   |    |
  |    |   /    |    \|    `   \/    |    \    |___|   |/        \  |    |
  |____|   \_______  /_______  /\_______  /_______ \___/_______  /  |____|
                   \/        \/         \/        \/           \/
"""
print(logo)

FILENAME = "hansimglück.pkl"

# Load todos
if os.path.exists(FILENAME):
    with open(FILENAME, "rb") as f:
        todos = pickle.load(f)
else:
    todos = []


def add_task():
    hans = 1
    print("Add your Task here, write exit to exit!")
    while hans == 1:
        task = input("")
        if task == "exit":
            break
        else:
            todos.append(task)


def show_todo():
    print(todos)


def remove_task():
    print(todos)
    task_remove = input("")
    if task_remove in todos:
        todos.remove(task_remove)
    else:
        print("This is not a valid input")


def app():
    while 1 == 1:
        print("--------------------------")
        print("What would you like to do?")
        print("--------------------------")
        print("1 (add a task)")
        print("2 (remove a task)")
        print("3 (show todolist)")
        print("--------------------------")
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

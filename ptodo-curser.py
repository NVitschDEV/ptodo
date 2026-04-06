#!/usr/bin/env python

import curses
import json
import os
import pickle

TODOLIST = "TODOLIST.json"
PICKLE_FILE = "theme_data_curses.pkl"
GROCERIES_FILE = "GROCERIES.json"

LOGO = [
    r"___________________  ________    ________  .____    .___  _______________________",
    r"\__    ___/\_____  \ \______ \   \_____  \ |    |   |   |/      _____/\__    ___/",
    r"  |    |    /   |   \ |    |  \   /   |   \|    |   |   |\_____  \      |    |   ",
    r"  |    |   /    |    \|    `   \ /    |    \    |___|   |/        \     |    |   ",
    r"  |____|   \_________/_________/ \_________/________\___/_________/     |____|   ",
]
GROCERIES_LOGO = [
    r"         "
    r"GROCERIES"
    r"         "
]


def load_todos():
    if os.path.exists(TODOLIST):
        try:
            with open(TODOLIST, "r") as f:
                data = json.load(f)
                for item in data:
                    if isinstance(item, dict) and "priority" not in item:
                        item["priority"] = "4"
                if data and isinstance(data[0], str):
                    return [{"task": t, "done": False, "priority": "4"} for t in data]
                data.sort(key=lambda x: (x.get("done", False), x.get("priority", "4")))
                return data
        except Exception:
            return []
    return []


def save_todos(todos):
    with open(TODOLIST, "w") as f:
        json.dump(todos, f, indent=4)


def draw_logo(stdscr, theme_id):
    themes = {
        "1": (6, 3),  # Catppuccin
        "2": (6, 5),  # Dracula
        "3": (1, 2),  # Gruvbox
        "4": (5, 3),  # Nord
    }
    c1_idx, c2_idx = themes.get(theme_id, (6, 3))

    h, w = stdscr.getmaxyx()
    for i, line in enumerate(LOGO):
        x = max(0, (w - len(line)) // 2)
        color = curses.color_pair(c1_idx) if i < 2 else curses.color_pair(c2_idx)
        try:
            stdscr.addstr(i + 1, x, line, color | curses.A_BOLD)
        except curses.error:
            pass


def draw_table(stdscr, todos, start_y):
    h, w = stdscr.getmaxyx()
    if not todos:
        msg = "No tasks found! Get to work!"
        try:
            stdscr.addstr(
                start_y,
                max(0, (w - len(msg)) // 2),
                msg,
                curses.color_pair(1) | curses.A_BOLD,
            )
        except curses.error:
            pass
        return start_y + 2

    header = f"{'#':<4} | {'Priority':<10} | {'Task':<30} | {'Status':>15}"
    row_x = max(0, (w - len(header)) // 2)

    try:
        stdscr.addstr(start_y, row_x, header, curses.color_pair(6) | curses.A_BOLD)
        stdscr.addstr(start_y + 1, row_x, "-" * len(header), curses.color_pair(6))
    except curses.error:
        pass

    y = start_y + 2
    for idx, item in enumerate(todos, 1):
        if y >= h - 8:
            break

        task_text = (
            item["task"][:27] + "..." if len(item["task"]) > 30 else item["task"]
        )
        prio_key = item.get("priority", "4")

        prio_map = {
            "1": ("High", curses.color_pair(1) | curses.A_BOLD),
            "2": ("Medium", curses.color_pair(2) | curses.A_BOLD),
            "3": ("Low", curses.color_pair(3) | curses.A_BOLD),
            "4": ("None", curses.color_pair(7) | curses.A_DIM),
        }
        p_lbl, p_color = prio_map.get(prio_key, prio_map["4"])

        if item.get("done"):
            status_lbl = "✔ Done"
            status_color = curses.color_pair(4) | curses.A_BOLD
            p_lbl = "-"
            p_color = curses.color_pair(7) | curses.A_DIM
            task_attr = curses.color_pair(7) | curses.A_DIM
        else:
            status_lbl = "Pending"
            status_color = curses.color_pair(2)
            task_attr = curses.color_pair(5)

        try:
            stdscr.addstr(y, row_x, f"{idx:<4} | ", curses.color_pair(7))
            stdscr.addstr(y, row_x + 7, f"{p_lbl:<10}", p_color)
            stdscr.addstr(y, row_x + 18, f"| {task_text:<30} | ", task_attr)
            stdscr.addstr(y, row_x + 53, f"{status_lbl:>13}", status_color)
        except curses.error:
            pass
        y += 1
    return y


def prompt_input(stdscr, prompt_text, y, x):
    stdscr.addstr(y, x, prompt_text, curses.color_pair(4) | curses.A_BOLD)
    try:
        curses.curs_set(1)
    except curses.error:
        pass
    curses.echo()

    stdscr.refresh()
    try:
        s = stdscr.getstr(y, x + len(prompt_text)).decode("utf-8")
    except Exception:
        s = ""

    curses.noecho()
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    return s


def select_list(stdscr, title, items, theme_id):
    current = 0
    while True:
        stdscr.clear()
        draw_logo(stdscr, theme_id)
        h, w = stdscr.getmaxyx()

        try:
            stdscr.addstr(
                8,
                max(0, (w - len(title)) // 2),
                title,
                curses.color_pair(6) | curses.A_BOLD,
            )
        except curses.error:
            pass

        max_visible = h - 12
        start_idx = max(0, current - max_visible // 2)
        end_idx = min(len(items), start_idx + max_visible)

        for i in range(start_idx, end_idx):
            lbl, val = items[i]
            y = 10 + (i - start_idx)
            x = max(0, (w - len(lbl)) // 2 - 2)
            try:
                if i == current:
                    stdscr.addstr(
                        y, x, f"> {lbl}", curses.color_pair(7) | curses.A_REVERSE
                    )
                else:
                    stdscr.addstr(y, x, f"  {lbl}", curses.color_pair(7))
            except curses.error:
                pass

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current > 0:
            current -= 1
        elif key == curses.KEY_DOWN and current < len(items) - 1:
            current += 1
        elif key in [10, 13]:  # Enter key
            return items[current][1]
        elif key == 27:  # Escape key
            return None


def add_mode(stdscr, todos, theme_id):
    stdscr.clear()
    draw_logo(stdscr, theme_id)
    draw_table(stdscr, todos, 8)
    h, w = stdscr.getmaxyx()

    task = prompt_input(stdscr, "Add Task (or 'exit'): ", h - 4, 2)
    if task and task.lower() != "exit":
        prio = prompt_input(
            stdscr,
            "Priority [1] High [2] Medium [3] Low [4] None (Default 4): ",
            h - 3,
            2,
        )
        if prio not in ["1", "2", "3", "4"]:
            prio = "4"
        todos.append({"task": task, "done": False, "priority": prio})
        save_todos(todos)


def complete_mode(stdscr, todos, theme_id):
    pending = [(i, t) for i, t in enumerate(todos) if not t["done"]]
    if not pending:
        return

    options = [(f"Task {i + 1}: {t['task']}", i) for i, t in pending]
    options.append(("EXIT", None))

    selected = select_list(stdscr, "Select a task to complete:", options, theme_id)
    if selected is not None:
        todos[selected]["done"] = True
        save_todos(todos)


def edit_mode(stdscr, todos, theme_id):
    stdscr.clear()
    draw_logo(stdscr, theme_id)
    draw_table(stdscr, todos, 8)
    h, w = stdscr.getmaxyx()

    task_num = prompt_input(stdscr, "Edit Number (or 'exit'): ", h - 4, 2)
    if task_num.isdigit():
        idx = int(task_num) - 1
        if 0 <= idx < len(todos):
            new_task = prompt_input(
                stdscr,
                f"New task name (Leave blank to keep '{todos[idx]['task']}'): ",
                h - 3,
                2,
            )
            if not new_task:
                new_task = todos[idx]["task"]

            new_prio = prompt_input(
                stdscr,
                f"Update Priority [1/2/3/4] (Current {todos[idx]['priority']}): ",
                h - 2,
                2,
            )
            if new_prio not in ["1", "2", "3", "4"]:
                new_prio = todos[idx]["priority"]

            todos[idx]["task"] = new_task
            todos[idx]["priority"] = new_prio
            save_todos(todos)


def remove_mode(stdscr, todos, theme_id):
    if not todos:
        return

    options = [(f"Task {i + 1}: {t['task']}", i) for i, t in enumerate(todos)]
    options.append(("EXIT", None))

    selected = select_list(stdscr, "Select a task to delete:", options, theme_id)
    if selected is not None:
        todos.pop(selected)
        save_todos(todos)


def removeAll_mode(stdscr, todos, theme_id):
    stdscr.clear()
    draw_logo(stdscr, theme_id)
    draw_table(stdscr, todos, 8)
    h, w = stdscr.getmaxyx()

    confirm = prompt_input(
        stdscr, "ARE YOU SURE? Type 'YES' to delete everything: ", h - 3, 2
    )
    if confirm == "YES":
        if os.path.exists(TODOLIST):
            os.remove(TODOLIST)
        todos.clear()


def draw_main_menu(stdscr):
    h, w = stdscr.getmaxyx()
    menu_lines = [
        " [1] Add Task     [2] Complete Task",
        " [3] Remove Task  [4] Edit Task    ",
        " [5] Remove All   [6] Settings     ",
        " [7] Exit         [8] Groceries    ",
    ]
    for i, line in enumerate(menu_lines):
        try:
            stdscr.addstr(
                h - 6 + i,
                max(0, (w - len(line)) // 2),
                line,
                curses.color_pair(7) | curses.A_BOLD,
            )
        except curses.error:
            pass

    try:
        msg = "Choose (1-8): "
        stdscr.addstr(h - 1, max(0, (w - len(msg)) // 2), msg, curses.color_pair(2))
    except curses.error:
        pass


def main(stdscr):
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    curses.start_color()
    try:
        curses.use_default_colors()
        bg = -1
    except curses.error:
        bg = curses.COLOR_BLACK

    # Standardize our colors
    curses.init_pair(1, curses.COLOR_RED, bg)
    curses.init_pair(2, curses.COLOR_YELLOW, bg)
    curses.init_pair(3, curses.COLOR_BLUE, bg)
    curses.init_pair(4, curses.COLOR_GREEN, bg)
    curses.init_pair(5, curses.COLOR_CYAN, bg)
    curses.init_pair(6, curses.COLOR_MAGENTA, bg)
    curses.init_pair(7, curses.COLOR_WHITE, bg)

    theme_id = "1"
    if os.path.exists(PICKLE_FILE):
        try:
            with open(PICKLE_FILE, "rb") as f:
                theme_id = pickle.load(f)
        except Exception:
            pass

    while True:
        todos = load_todos()
        stdscr.clear()
        draw_logo(stdscr, theme_id)
        draw_table(stdscr, todos, start_y=8)
        draw_main_menu(stdscr)
        stdscr.refresh()

        key = stdscr.getch()

        if key == ord("1"):
            add_mode(stdscr, todos, theme_id)
        elif key == ord("2"):
            complete_mode(stdscr, todos, theme_id)
        elif key == ord("3"):
            remove_mode(stdscr, todos, theme_id)
        elif key == ord("4"):
            edit_mode(stdscr, todos, theme_id)
        elif key == ord("5"):
            removeAll_mode(stdscr, todos, theme_id)
        elif key == ord("6"):
            options = [
                ("Catppuccin (Mocha)", "1"),
                ("Dracula", "2"),
                ("Gruvbox", "3"),
                ("Nord", "4"),
                ("Cancel", None),
            ]
            res = select_list(stdscr, "Choose a Color Scheme:", options, theme_id)
            if res:
                theme_id = res
                with open(PICKLE_FILE, "wb") as f:
                    pickle.dump(theme_id, f)
        elif key in [ord("7"), 27]:
            break
        elif key == ord("8"):
            curses.wrapper(sort_groceries_auto)


"""""" """""" """"""


def sort_groceries_auto(stdscr):
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    curses.start_color()
    try:
        curses.use_default_colors()
        bg = -1
    except curses.error:
        bg = curses.COLOR_BLACK

    # Standardize our colors
    curses.init_pair(1, curses.COLOR_RED, bg)
    curses.init_pair(2, curses.COLOR_YELLOW, bg)
    curses.init_pair(3, curses.COLOR_BLUE, bg)
    curses.init_pair(4, curses.COLOR_GREEN, bg)
    curses.init_pair(5, curses.COLOR_CYAN, bg)
    curses.init_pair(6, curses.COLOR_MAGENTA, bg)
    curses.init_pair(7, curses.COLOR_WHITE, bg)

    theme_id = "1"

    # fix it with json GROCERIES_FILE save the keywords
    # if os.path.exists(GROCERIES_FILE):
    #    try:
    #        with open(GROCERIES_FILE, "r") as f:
    #            category_keywords = json.load(f)
    #   except Exception:
    #       pass

    """
    A Python program that helps you sort your groceries into categories,
    with an automatic sorting feature based on keywords.
    """

    category_keywords = {
        "Fruits": [
            "apple",
            "banana",
            "orange",
            "grape",
            "strawberry",
            "blueberry",
            "raspberry",
            "lemon",
            "lime",
            "peach",
            "pear",
            "mango",
            "pineapple",
            "kiwi",
            "melon",
            "cherry",
            "avocado",
            "plum",
            "fig",
            "apricot",
            "cranberry",
            "date",
            "pomegranate",
        ],
        "Vegetables": [
            "carrot",
            "broccoli",
            "spinach",
            "lettuce",
            "tomato",
            "cucumber",
            "onion",
            "garlic",
            "potato",
            "sweet potato",
            "bell pepper",
            "zucchini",
            "eggplant",
            "cabbage",
            "kale",
            "celery",
            "mushroom",
            "corn",
            "peas",
            "green bean",
            "asparagus",
            "brussels sprout",
            "cauliflower",
            "squash",
            "ginger",
            "chili",
            "jalapeno",
            "artichoke",
            "radish",
            "beet",
            "leek",
            "bok choy",
        ],
        "Dairy & Eggs": [
            "milk",
            "cheese",
            "yogurt",
            "butter",
            "egg",
            "cream",
            "sour cream",
            "cottage cheese",
            "cream cheese",
            "ghee",
            "kefir",
            "creamer",
            "margarine",
            "feta",
            "cheddar",
            "mozzarella",
            "Quark",
        ],
        "Meat & Seafood": [
            "chicken",
            "beef",
            "sausage",
            "ham",
            "turkey",
            "fish",
            "salmon",
            "tuna",
            "shrimp",
            "crab",
            "scallop",
            "lamb",
            "steak",
            "ground beef",
            "hot dog",
            "salami",
            "pepperoni",
            "cod",
            "tilapia",
            "oyster",
            "clams",
        ],
        "Pantry Items": [
            "pasta",
            "rice",
            "flour",
            "sugar",
            "salt",
            "pepper",
            "oil",
            "vinegar",
            "canned",
            "soup",
            "sauce",
            "cereal",
            "oats",
            "tortilla",
            "coffee",
            "tea",
            "jam",
            "honey",
            "spices",
            "nuts",
            "beans",
            "lentils",
            "broth",
            "syrup",
            "baking soda",
            "baking powder",
            "ketchup",
            "mustard",
            "mayonnaise",
            "crackers",
            "granola",
            "dried fruit",
            "peanut butter",
            "almond butter",
            "soy sauce",
            "olive oil",
            "vegetable oil",
            "quinoa",
            "couscous",
            "brownie mix",
            "cake mix",
            "chocolate chips",
            "gelatin",
            "cornstarch",
            "yeast",
            "olives",
            "pickles",
            "chips",
            "cookies",
            "salsa",
        ],
        "Frozen Foods": [
            "ice cream",
            "frozen pizza",
            "frozen vegetable",
            "frozen fruit",
            "frozen meal",
            "waffle",
            "fries",
            "tater tot",
            "burrito",
            "nuggets",
            "fish sticks",
            "hash brown",
            "popsicle",
            "sorbet",
            "ice",
            "dough",
            "smoothie mix",
        ],
        "Beverages": [
            "juice",
            "soda",
            "water",
            "beer",
            "wine",
            "cola",
            "sparkling water",
            "tea bag",
            "coffee grounds",
            "energy drink",
            "sports drink",
            "liquer",
            "seltzer",
            "kombucha",
            "almond milk",
            "soy milk",
            "oat milk",
        ],
        "Snacks": [
            "chips",
            "cookie",
            "cracker",
            "bar",
            "candy",
            "chocolate",
            "popcorn",
            "pretzels",
            "nuts",
            "granola bar",
            "fruit snack",
            "gummy",
            "jerky",
            "trail mix",
            "rice cakes",
            "wafers",
        ],
        "Bakery": [
            "bread",
            "bagel",
            "muffin",
            "croissant",
            "donut",
            "pastry",
            "pie",
            "cupcake",
            "sourdough",
            "rolls",
            "buns",
            "tarts",
            "bread",
        ],
        "Household & Personal Care": [
            "soap",
            "shampoo",
            "conditioner",
            "toothpaste",
            "brush",
            "detergent",
            "cleaner",
            "toilet paper",
            "paper towel",
            "sponge",
            "lotion",
            "razor",
            "tissue",
            "trash bag",
            "dish soap",
            "hand soap",
            "deodorant",
            "mouthwash",
            "laundry",
            "fabric softener",
            "bleach",
            "disinfectant",
            "air freshener",
            "light bulb",
            "battery",
            "aluminum foil",
            "plastic wrap",
            "ziploc",
            "band-aid",
            "medicine",
            "vitamins",
            "shaving cream",
        ],
    }

    # This ensures all categories are present in the final output, even if empty
    sorted_groceries = {category: [] for category in category_keywords}

    print("=" * 40)
    print(" Welcome to your Smart Grocery Sorter! ")
    print("=" * 40)
    print("Enter your grocery items one by one. Type 'done' when you're finished.")
    print("The program will try to automatically sort items based on keywords.")
    print("If it can't find a match, you'll be asked to choose a category manually.")
    print("-" * 40)

    # Display available categories for manual selection (if needed)
    category_names_for_manual_selection = list(category_keywords.keys())
    print("Available categories for manual sorting (if needed):")
    for i, cat in enumerate(category_names_for_manual_selection):
        print(f"  {i + 1}. {cat}")
    print("-" * 40)

    while True:
        item_input = input("Enter grocery item (or 'done' to finish): ").strip()

        if item_input.lower() == "done":
            break
        if not item_input:  # Handle empty input for item name
            print("Please enter an item name.")
            continue

        item_normalized = item_input.lower()
        assigned_automatically = False

        # Attempt automatic sorting
        # We iterate through categories, and for each category, check if any of its
        # keywords are present in the entered item name.
        for category, keywords in category_keywords.items():
            # The 'if keyword' ensures we don't try to match against an empty string keyword
            if any(keyword in item_normalized for keyword in keywords if keyword):
                sorted_groceries[category].append(item_input)
                print(f"'{item_input}' automatically added to '{category}'.")
                assigned_automatically = True
                break  # Item found and assigned, move to the next grocery input

        # If no automatic match was found, ask the user to choose a category
        if not assigned_automatically:
            category_names_for_manual_selection = list(category_keywords.keys())
            print("Available categories for manual sorting (if needed):")
            for i, cat in enumerate(category_names_for_manual_selection):
                print(f"  {i + 1}. {cat}")
            print("-" * 40)
            print(
                f"Could not automatically sort '{item_input}'. Please choose a category:"
            )

            while True:
                category_choice = input(
                    f"Which category does '{item_input}' belong to? (Enter number or category name): "
                ).strip()

                chosen_category = None

                # Try to match by number
                if category_choice.isdigit():
                    idx = int(category_choice) - 1
                    if 0 <= idx < len(category_names_for_manual_selection):
                        chosen_category = category_names_for_manual_selection[idx]
                else:
                    # Try to match by category name (case-insensitive)
                    for cat_name in category_names_for_manual_selection:
                        if category_choice.lower() == cat_name.lower():
                            chosen_category = cat_name
                            break

                if chosen_category:
                    sorted_groceries[chosen_category].append(item_input)
                    print(f"'{item_input}' manually added to '{chosen_category}'.")
                    break  # Exit inner loop, go to next item
                else:
                    print(
                        "Invalid category choice. Please enter a valid number or category name from the list."
                    )

    print("" + "=" * 40)
    print(" Your Sorted Groceries: ")
    print("=" * 40)

    # Display the sorted groceries
    found_items = False
    for category, items in sorted_groceries.items():
        if items:  # Only print categories that have items
            found_items = True
            print(f"--- {category} ---")
            for item in items:
                print(f"- {item}")

    if not found_items:
        print("No items were entered or sorted.")

    print("" + "=" * 40)
    print(" Happy organizing! ")
    print("=" * 40)


"""""" """""" """"""

if __name__ == "__main__":
    curses.wrapper(main)

import typer
from storage import print_tasks_table


def print_menu() -> None:
    print("\n=== Task Manager (CLI MVP) ===")
    print("1) Add a task")
    print("2) List tasks")
    print("3) Mark task as complete")
    print("4) Exit")


def main():
    app = typer.Typer()
    running = True
    tasks = []

    while running:
        
        try:
            option = int(input("Choose an option: "))
        except ValueError:
            print("Not valid input. It has to be a number.")
            continue

        if option == 1:
            print("\n=== Add a New Task ===")
            title = input("Title (required): ").strip()
            while not title:
                print("Title cannot be empty.")
                title = input("Title (required): ").strip()

            description = input("Description (optional): ").strip()

            due_date = input("Due date (YYYY-MM-DD) or leave blank: ").strip()
            priority = input(
                "Priority (Low/Medium/High) or leave blank for Medium: "
            ).strip()

        elif option == 2:
            print_tasks_table(tasks)

        elif option == 3:
            pass
        elif option == 4:
            running = False
        else:
            print("Invalid option. Choose 1-4.")


if __name__ == "__main__":
    typer.run(main)

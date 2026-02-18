"""
PART E — Production Simulation: Command-Line Expense Tracker
Guide: docs/python-guide/01-foundations.md

Build a complete expense tracker that:
1. Add expenses (amount, category, description)
2. View all expenses (formatted table)
3. View expenses by category
4. Show summary (total, by category, monthly)
5. Save/load data to/from a file

Acceptance Criteria:
- [ ] Uses functions (no code in global scope except main)
- [ ] Input validation (no negative amounts, no empty categories)
- [ ] Clean formatting with f-strings
- [ ] Uses dicts and lists appropriately
- [ ] Handles edge cases (empty data, invalid input)
"""

from datetime import datetime


def add_expense(expenses: list, amount: float, category: str, description: str) -> dict:
    """Add a new expense and return it."""
    # TODO: Implement
    pass


def get_expenses_by_category(expenses: list, category: str) -> list:
    """Filter expenses by category."""
    # TODO: Implement
    pass


def get_summary(expenses: list) -> dict:
    """Calculate summary statistics."""
    # TODO: Implement — total, by category, count
    pass


def print_expenses(expenses: list):
    """Print expenses as a formatted table."""
    # TODO: Implement
    pass


def print_summary(expenses: list):
    """Print a summary report."""
    # TODO: Implement
    pass


def main():
    """Main menu loop."""
    expenses = []

    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. View by category")
        print("4. Summary")
        print("5. Quit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            # TODO: Get input and add expense
            pass
        elif choice == "2":
            print_expenses(expenses)
        elif choice == "3":
            # TODO: Ask for category and show filtered
            pass
        elif choice == "4":
            print_summary(expenses)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

import csv
from datetime import datetime
from pathlib import Path
from collections import defaultdict

DATA_FILE = Path("expenses.csv")

CATEGORIES = [
    "Food", "Travel", "Education",
    "Shopping", "Bills", "Health", "Other"
]


def load_expenses():
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", newline="") as file:
        return list(csv.DictReader(file))


def save_expenses(expenses):
    with open(DATA_FILE, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["date", "category", "description", "amount"]
        )
        writer.writeheader()
        writer.writerows(expenses)


def add_expense():
    print("\n--- Add New Expense ---")

    date = input("Enter date (YYYY-MM-DD): ")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date!")
        return

    print("\nCategories:")
    for i, category in enumerate(CATEGORIES, 1):
        print(f"{i}. {category}")

    try:
        choice = int(input("Choose category: "))
        category = CATEGORIES[choice - 1]

        if choice < 1 or choice > len(CATEGORIES):
            print("Invalid category!")
            return
    except (ValueError, IndexError):
        print("Invalid category!")
        return

    description = input("Enter description: ")

    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be positive!")
            return
    except ValueError:
        print("Invalid amount!")
        return

    expenses = load_expenses()

    expenses.append({
        "date": date,
        "category": category,
        "description": description,
        "amount": amount
    })

    save_expenses(expenses)
    print("Expense added successfully!")


def view_expenses():
    expenses = load_expenses()

    print("\n--- Expense History ---")

    if not expenses:
        print("No expenses found.")
        return

    for i, expense in enumerate(expenses, 1):
        print(
            f"{i}. {expense['date']} | "
            f"{expense['category']} | "
            f"{expense['description']} | "
            f"Rs.{float(expense['amount']):.2f}"
        )

    total = sum(float(e["amount"]) for e in expenses)
    print(f"\nTotal Expenses: Rs.{total:.2f}")


def monthly_summary():
    month = input("Enter month (YYYY-MM): ")

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format!")
        return

    expenses = load_expenses()

    monthly = [
        e for e in expenses if e["date"].startswith(month)
    ]

    total = sum(float(e["amount"]) for e in monthly)

    print("\n--- Monthly Summary ---")
    print("Month:", month)
    print("Transactions:", len(monthly))
    print(f"Total Spent: Rs.{total:.2f}")


def category_summary():
    expenses = load_expenses()
    totals = defaultdict(float)

    for expense in expenses:
        totals[expense["category"]] += float(expense["amount"])

    grand_total = sum(totals.values())

    print("\n--- Category-wise Summary ---")

    if not expenses:
        print("No expenses found.")
        return

    for category, amount in sorted(
        totals.items(), key=lambda x: x[1], reverse=True
    ):
        percentage = amount / grand_total * 100
        print(
            f"{category}: Rs.{amount:.2f} "
            f"({percentage:.1f}%)"
        )


def delete_expense():
    expenses = load_expenses()

    if not expenses:
        print("No expenses available.")
        return

    view_expenses()

    try:
        number = int(input("Enter expense number to delete: "))

        if number < 1 or number > len(expenses):
            print("Invalid expense number!")
            return

        removed = expenses.pop(number - 1)
        save_expenses(expenses)

        print(f"Deleted: {removed['description']}")

    except ValueError:
        print("Enter a valid number!")


def main():
    while True:
        print("\n====== SMART EXPENSE TRACKER ======")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Summary")
        print("4. Category Summary")
        print("5. Delete Expense")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("Thank you for using Smart Expense Tracker!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()

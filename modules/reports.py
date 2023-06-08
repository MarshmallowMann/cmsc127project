import mariadb as db
from tabulate import tabulate
import modules.group as group
import modules.friend as friend


def view_all_expenses_within_month(cursor: db.Cursor) -> None:

    transaction_date = friend.get_int_input("Enter the month to view: ")

    try:
        cursor.execute(
            "SELECT * FROM transaction WHERE MONTH(transaction_date) = ?;", (transaction_date,))
        expenses = cursor.fetchall()

    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    print_expenses(expenses)
    return None


def view_all_expenses_made_with_friend(cursor: db.Cursor) -> None:
    return None


def view_all_expenses_with_group(cursor: db.Cursor) -> None:
    group_id = group.get_int_input("Enter group id: ")

    try:
        cursor.execute(
            "SELECT * FROM transaction WHERE group_id = ?;", (group_id,))
        expenses = cursor.fetchall()

    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    print_expenses(expenses)
    return None


def view_current_balance(cursor: db.Cursor) -> None:

    try:
        cursor.execute("SELECT * FROM user WHERE user_id = 1;")
        self = cursor.fetchall()

    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    print_self(self)
    return None


def view_all_friends_with_balance(cursor: db.Cursor) -> None:
    try:
        cursor.execute(
            "SELECT * FROM user WHERE user_id != 1 AND balance > 0;")
        friends = cursor.fetchall()

    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    friend.print_users(friends)
    return None


def view_all_groups(cursor: db.Cursor) -> None:

    try:
        cursor.execute("SELECT * FROM `group`;")
        groups = cursor.fetchall()

    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    group.print_groups(groups)
    return None


def view_all_groups_with_balance(cursor: db.Cursor) -> None:

    try:
        cursor.execute("SELECT * FROM `group` WHERE group_balance > 0;")
        groups = cursor.fetchall()

    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    group.print_groups(groups)
    return None


def print_self(self: list) -> None:
    # Convert array of tuples to array of lists
    # friends = [list(friend) for friend in friends]
    print("=====================================")
    print("\t\tUser")
    print("=====================================")
    print(tabulate(self, headers=[
          "ID", "Username", "Balance"], tablefmt="rounded_grid"))
    print("=====================================")
    return None


def print_expenses(expenses: list) -> None:
    print("=====================================")
    print("\t\tExpenses")
    print("=====================================")
    print(tabulate(expenses, headers=[
          "Transaction ID", "Transaction Amount", "Transaction Date",
          "Trasanction Type", "isLoan", "lender",
          "isGroupLoan", "amountRemaining", "dividedAmount",
          "isSettlement", "settledLoan", "user_id", "group_id"
          ], tablefmt="rounded_grid"))
    print("=====================================")
    return None

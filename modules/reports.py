import mariadb as db
from tabulate import tabulate
import modules.group as group
import modules.friend as friend


# Print all the expenses within a certain month
def view_all_expenses_within_month(cursor: db.Cursor) -> None:

    # Get the month from the user
    transaction_date = friend.get_int_input("Enter the month to view: ")

    try:
        # Fetch the expenses from the database
        cursor.execute(
            "SELECT * FROM transaction WHERE MONTH(transaction_date) = ?;", (transaction_date,))
        expenses = cursor.fetchall()

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    # Print the expenses
    print_expenses(expenses)
    return None


# Print all the expenses made with a friend
def view_all_expenses_made_with_friend(cursor: db.Cursor) -> None:
    return None


# Print all the expenses made with a group
def view_all_expenses_with_group(cursor: db.Cursor) -> None:

    # Get the group id from the user
    group_id = group.get_int_input("Enter group id: ")

    try:
        # Fetch the expenses from the database
        cursor.execute(
            "SELECT * FROM transaction WHERE group_id = ?;", (group_id,))
        expenses = cursor.fetchall()

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    # Print the expenses
    print_expenses(expenses)
    return None


# Print user's current balance
def view_current_balance(cursor: db.Cursor) -> None:

    try:
        # Fetch the user's balance from the database
        cursor.execute("SELECT * FROM user WHERE user_id = 1;")
        self = cursor.fetchall()

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    # Print the user's balance
    print_self(self)
    return None


# Print all the friends with balance in the database
def view_all_friends_with_balance(cursor: db.Cursor) -> None:
    try:
        # Fetch the friends with balance from the database
        cursor.execute(
            "SELECT * FROM user WHERE user_id != 1 AND balance > 0;")
        friends = cursor.fetchall()

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    # Print the friends with balance
    friend.print_users(friends)
    return None


# Print all the groups in the database
def view_all_groups(cursor: db.Cursor) -> None:

    try:
        # Fetch the groups from the database
        cursor.execute("SELECT * FROM `group`;")
        groups = cursor.fetchall()

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    # Print the groups
    group.print_groups(groups)
    return None


# Print all the groups with balance in the database
def view_all_groups_with_balance(cursor: db.Cursor) -> None:

    try:
        # Fetch the groups with balance from the database
        cursor.execute("SELECT * FROM `group` WHERE group_balance > 0;")
        groups = cursor.fetchall()

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    # Print the groups with balance
    group.print_groups(groups)
    return None


# Print user balance
def print_self(self: list) -> None:
    print("=====================================")
    print("\t\tUser")
    print("=====================================")
    print(tabulate(self, headers=[
          "ID", "Username", "Balance"], tablefmt="rounded_grid"))
    print("=====================================")
    return None


# Print expenses
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

import mariadb as db
from tabulate import tabulate
import modules.group as group
import modules.friend as friend


# Print all the expenses within a certain month
def view_all_expenses_within_month(cursor: db.Cursor) -> None:

    while True:
        # Get the month from the user
        transaction_date = friend.get_int_input("Enter the month to view: ")

        if transaction_date < 1 or transaction_date > 12:
            print("Invalid month.")
            continue

        else:
            break

    try:
        # Fetch the expenses from the database
        cursor.execute(
            "SELECT transaction_id, transaction_amount, transaction_date, transaction_type, isLoan, lender, amountRemaining, dividedAmount, isSettlement, settledLoan, user_id, group_id FROM transaction WHERE MONTH(transaction_date) = ?;", (transaction_date,))
        expenses = cursor.fetchall()

        # If there are no groups in the database, return None
        if len(expenses) <= 0:
            print("There are no expenses in the database.")
            return None

        # Print the expenses
        print_expenses(expenses)
        return None

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None


# Print all the expenses made with a friend
def view_all_expenses_made_with_friend(cursor: db.Cursor) -> None:

    try:
        # Fetch all the friends in the database
        cursor.execute("SELECT * FROM user WHERE user.user_id != 1;")
        friends = cursor.fetchall()

        # If there are no groups in the database, return None
        if len(friends) <= 0:
            print("There are no friends in the database.")
            return None

        # Print all the friends in the database
        friend.print_users(friends)

    # If there is an error, prompt the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    friend_id = friend.get_int_input("Enter friend id: ")

    try:
        # Fetch the user's balance from the database
        cursor.execute(
            "SELECT * FROM transaction WHERE (user_id=1 AND lender=?) OR (lender=1 AND user_id=?) ")
        friends = cursor.fetchall()

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    # Print all the friends in the database
    friend.print_users(friends)
    return None


# Print all the expenses made with a group
def view_all_expenses_with_group(cursor: db.Cursor) -> None:

    view_all_groups(cursor)

    # Get the group id from the user
    group_id = group.get_int_input("Enter group id: ")

    try:
        # Fetch the expenses from the database
        cursor.execute(
            "SELECT transaction_id, transaction_amount, transaction_date, transaction_type, isLoan, lender, amountRemaining, dividedAmount, isSettlement, settledLoan, user_id, group_id FROM transaction WHERE group_id = ?;", (group_id,))
        expenses = cursor.fetchall()

        # If there are no groups in the database, return None
        if len(expenses) <= 0:
            print("There are no expenses in the database.")
            return None

        # Print the expenses
        print_expenses(expenses)
        return None

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
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

        # If there are no groups in the database, return None
        if len(friends) <= 0:
            print("There are no friends with remaining balance in the database.")
            return None

        # Print the friends with balance
        friend.print_users(friends)
        return None

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None


# Print all the groups in the database
def view_all_groups(cursor: db.Cursor) -> None:

    try:
        # Fetch the groups from the database
        cursor.execute("SELECT * FROM `group`;")
        groups = cursor.fetchall()

        # If there are no groups in the database, return None
        if len(groups) <= 0:
            print("There are no groups in the database.")
            return None

        # Print the groups
        group.print_groups(groups)
        return None

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None


# Print all the groups with balance in the database
def view_all_groups_with_balance(cursor: db.Cursor) -> None:

    try:
        # Fetch the groups with balance from the database
        cursor.execute("SELECT * FROM `group` WHERE group_balance > 0;")
        groups = cursor.fetchall()

        # If there are no groups in the database, return None
        if len(groups) <= 0:
            print("There are no groups with balance in the database.")
            return None

        # Print the groups with balance
        group.print_groups(groups)
        return None

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
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


def print_expenses(expenses: list) -> None:
    # SELECT user_id, transaction_id, transaction_amount, transaction_date, lender
    print("=====================================")
    print("\t\tExpenses")
    print(tabulate(expenses, headers=["Transaction Id", "Transaction Amount", "Transaction Date", "Transaction Type",
                                      "Is Loan", "Lender", "Amount Remaining", "Divided Amount", "isSettlement", "Settled Loan", "User ID", "Group ID"], tablefmt="rounded_grid"))
    print("=====================================")
    return None

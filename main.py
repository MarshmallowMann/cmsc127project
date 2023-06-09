import mariadb as db
import sys
import os
from dotenv import load_dotenv

import modules.expense as expense
import modules.friend as friend
import modules.group as group
import modules.reports as report

"""
Given the description and the details below, come up with flexible and realistic database
design, and a good implementation, in any chosen PL and RDBMS by the team, in order to create
the project.

Features:
1. Add, delete, search, and update an expense;
2. Add, delete, search, and update a friend;
3. Add, delete, search, and update a group
Reports to be generated:
1. View all expenses made within a month;
2. View all expenses made with a friend;
3. View all expenses made with a group;
4. View current balance from all expenses;
5. View all friends with outstanding balance;
6. View all groups;
7. View all groups with an outstanding balance

Relational Model:
TRANSACTION(Transaction id, Amount, Date, Transaction type, Is loan, Lender, Is paid, Is 
group loan, Amount remaining, Divided amount, Is settlement, Settled loan, User id, Group id)
USER (User id, Username, User current balance)
GROUP (Group id, Num of members, Group name, Group current balance)
IS_PART_OF (User id, Group id)
IS_CREATED_BY (Transaction id, User id, Group id)

"""


def main():

    print("Hello World!")

    try:
        conn = db.connect(
            user="root",
            password=os.environ.get('PASSWORD'),
            host="localhost",
            database="loan_tracker")
    except db.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    cur = conn.cursor()

    while True:
        print_menu()

        choice = get_int_input("Enter your choice: ")
        print(f"Choice: {choice}")
        if choice == 1:
            print_expense_menu(cur, conn)
        elif choice == 2:
            print_friend_menu(cur, conn)
        elif choice == 3:
            print_group_menu(cur, conn)
        elif choice == 4:
            print_report_menu(cur, conn)
        elif choice == 0:
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")


def print_menu() -> None:
    print(
        """
Enter a number:
[1] Add, delete, search, and update an expense
[2] Add, delete, search, and update a friend
[3] Add, delete, search, and update a group
---------------------------------------------
[4]  Generate Reports

[0] Exit
""")
    return None


def print_expense_menu(cur: db.Cursor, con: db.Connection) -> None:
    print(
        """
[1] Add an expense
[2] Delete an expense
[3] Search an expense
[4] Update an expense

[0] Back    
""")

    choice = get_int_input("Enter your choice: ")

    if choice == 1:
        expense.add_expense(cur, con)
    elif choice == 2:
        expense.delete_expense(cur, con)
    elif choice == 3:
        expense.search_expense(cur)
    elif choice == 4:
        expense.update_expense(cur, con)
    elif choice == 0:
        return None


def print_friend_menu(cur: db.Cursor, con: db.Connection) -> None:
    print(
        """
[1] Add an friend
[2] Delete an friend
[3] Search an friend
[4] Update an friend

[0] Back    
""")

    choice = get_int_input("Enter your choice: ")

    if choice == 1:
        friend.add_friend(cur, con)
    elif choice == 2:
        friend.delete_friend(cur, con)
    elif choice == 3:
        friend.search_friend(cur, con)
    elif choice == 4:
        friend.update_friend(cur, con)
    elif choice == 0:
        cur.close()
        return None


def print_group_menu(cur: db.Cursor, con: db.Connection) -> None:
    print(
        """
[1] Add an group
[2] Delete an group
[3] Search an group
[4] Update an group

[0] Back    
""")

    choice = get_int_input("Enter your choice: ")

    if choice == 1:
        group.add_group(cur, con)
    elif choice == 2:
        group.delete_group(cur, con)
    elif choice == 3:
        group.search_group(cur)
    elif choice == 4:
        group.update_group(cur, con)
    elif choice == 0:
        return None


def print_report_menu(cur: db.Cursor, con: db.Connection) -> None:
    print(
        """
[1] View all expenses made within a month
[2] View all expenses made with a friend
[3] View all expenses made with a group
[4] View current balance from all expenses
[5] View all friends with outstanding balance
[6] View all groups
[7] View all groups with an outstanding balance

[0] Back
    """
    )

    choice = get_int_input("Select report to generate: ")

    if choice == 1:
        report.view_all_expenses_within_month(cur)
    elif choice == 2:
        report.view_all_expenses_made_with_friend(cur)
    elif choice == 3:
        report.view_all_expenses_with_group(cur)
    elif choice == 4:
        report.view_current_balance(cur)
    elif choice == 5:
        report.view_all_friends_with_balance(cur)
    elif choice == 6:
        report.view_all_groups(cur)
    elif choice == 7:
        report.view_all_groups_with_balance(cur)
    elif choice == 0:
        return None


def get_int_input(prompt: str) -> int:
    while True:
        try:
            num = int(input(prompt))
            return num
        except ValueError:
            print("Invalid input. Please try again.")


if __name__ == "__main__":
    load_dotenv()
    main()

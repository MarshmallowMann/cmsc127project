import mariadb as db
import sys
import os
from dotenv import load_dotenv
import modules.group as group

"""
Given the description and the details below, come up with flexible and realistic database
design, and a good implementation, in any chosen PL and RDBMS by the team, in order to create
the project.
"""


def main():

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
    # group.add_group(cur, conn)
    # group.delete_group(cur, conn)
    # group.search_group(cur, conn)
    group.get_groups(cur, conn)


"""
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
"""


def print_menu() -> None:
    print("""

    1. Add, delete, search, and update an expense
    2. Add, delete, search, and update a friend
    3. Add, delete, search, and update a group
    """)
    return None


if __name__ == "__main__":
    load_dotenv()
    main()

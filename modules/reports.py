import mariadb as db


def viewAllExpensesWithinMonth(cursor: db.Cursor) -> None:
    return None


def viewAllExpensesWithFriend(cursor: db.Cursor) -> None:
    return None


def viewAllExpensesWithGroup(cursor: db.Cursor) -> None:
    return None


def viewCurrentBalance(cursor: db.Cursor) -> None:
    return None


def viewAllFriendsWithBalance(cursor: db.Cursor) -> None:
    return None


def viewAllGroups(cursor: db.Cursor) -> None:

    print("===========================================")
    print("GROUPS IN THE DATABASE")

    try:
        statement = "SELECT * FROM `group`;"
        cursor.execute(statement)

        # iterate over the users
        for i, row in enumerate(cursor):
            group_id = row[0]
            group_name = row[1]
            group_balance = row[2]
            num_of_members = row[3]

            print(
                f"Id: {group_id} | Name: {group_name} | Balance: {group_balance} | Number of members: {num_of_members}")

    except db.Error as e:
        print(f"\nError retrieving users from the database: {e}")

    print("===========================================\n")
    return None


def viewAllGroupsWithBalance(cursor: db.Cursor) -> None:

    print("===========================================")
    print("GROUPS IN THE DATABASE WITH OUTSTANDING BALANCE")

    try:
        statement = "SELECT * FROM `group` WHERE group_balance>0;"
        cursor.execute(statement)

        # iterate over the users
        for i, row in enumerate(cursor):
            group_id = row[0]
            group_name = row[1]
            group_balance = row[2]
            num_of_members = row[3]

            print(
                f"Id: {group_id} | Name: {group_name} | Balance: {group_balance} | Number of members: {num_of_members}")

    except db.Error as e:
        print(f"\nError retrieving users from the database: {e}")

    print("===========================================\n")
    return None

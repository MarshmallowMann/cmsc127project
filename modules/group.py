import mariadb as db


def addGroup(cursor: db.Cursor, conn: db.Connection) -> None:

    while True:
        try:                 # get ready to catch exceptions inside here
            group_name = input("Enter group name: ")
            group_balance = float(input("Enter group balance: "))
            num_of_members = int(input("Enter number of members: "))
        except ValueError as e:
            print(f"Error: {e}\n")
        else:                # <-- no exception. break
            break

    try:
        statement = "INSERT INTO `group`(group_name, group_balance, num_of_members) VALUES(?, ?, ?);"
        data = (group_name, group_balance, num_of_members)
        cursor.execute(statement, data)
        conn.commit()
        print("Successfully added group to the database")
    except db.Error as e:
        print(f"Error adding group to the database: {e}")
        conn.rollback()

    return None


# medj eme eme pa sksksks
def delete_group(cursor: db.Cursor, conn: db.Connection) -> None:

    get_groups(cursor, conn)

    while True:
        try:
            group_id = int(input("Enter the group id to delete: "))
        except ValueError as e:
            print(f"Error: {e}\n")
        else:
            break

    try:
        statement = "DELETE FROM `group` WHERE group_id = ?;"
        data = (group_id,)
        cursor.execute(statement, data)
        conn.commit()
        print("Successfully deleted group from the database")
    except db.Error as e:
        print(f"Error deleting group from the database: {e}")
        conn.rollback()

    return None


def search_group(cursor: db.Cursor, conn: db.Connection) -> None:

    while True:
        try:
            group_id = int(input("Enter the id of the group to search: "))
        except ValueError as e:
            print(f"Error: {e}\n")
        else:
            break

    try:
        statement = "SELECT * FROM `group` WHERE group_id = ?;"
        data = (group_id,)
        cursor.execute(statement, data)

        row = cursor.fetchone()

        if row is not None:
            group_id = row[0]
            group_name = row[1]
            group_balance = row[2]
            num_of_members = row[3]
            print(
                f"Id: {group_id} | Name: {group_name} | Balance: {group_balance} | Number of members: {num_of_members}")

    except db.Error as e:
        print(f"Error retrieving group from the database: {e}")

    return None


def updateGroup(cursor: db.Cursor, conn: db.Connection) -> None:
    return None


def get_groups(cursor: db.Cursor, conn: db.Connection) -> None:
    try:
        statement = "SELECT group_id, group_name FROM `group`;"
        cursor.execute(statement)
        print("Groups:")

        # iterate over the users
        for i, j, row in enumerate(cursor):

            i = row

            group_id = i[0]
            group_name = i[1]
            # start with the second user because the first user is the one using the app
            print(f"[{j}]  {group_id} - {group_name}")

    except db.Error as e:
        print(f"Error retrieving users from the database: {e}")

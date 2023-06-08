import mariadb as db


def addGroup(cursor: db.Cursor, conn: db.Connection) -> None:

    print("===========================================")
    print("ADD A NEW GROUP TO THE DATABASE")

    while True:
        try:
            group_name = get_string_input("Enter the group name: ")

        except ValueError as e:
            print(f"Error: {e}\n")

        else:
            break

    try:
        statement = "INSERT INTO `group`(group_name) VALUES(?);"
        data = (group_name,)
        cursor.execute(statement, data)

        conn.commit()

        statement = "SELECT group_id FROM `group` WHERE group_name = ?;"
        data = (group_name,)
        cursor.execute(statement, data)

        group_id = cursor.fetchone()[0]

        statement = "INSERT INTO is_part_of(user_id, group_id) VALUES(1, ?);"
        data = (group_id,)
        cursor.execute(statement, data)

        addFriendToGroup(cursor, conn, group_id)

        print("\nSuccessfully added group to the database")

    except db.Error as e:
        print(f"\nError adding group to the database: {e}")
        conn.rollback()

    print("===========================================\n")
    return None


def deleteGroup(cursor: db.Cursor, conn: db.Connection) -> None:

    if getGroups(cursor, conn) > 0:
        try:
            while True:
                group_id = int(
                    input("\nEnter the id of the group to delete: "))

                if group_id == 0:
                    print("===========================================\n")
                    return None

                statement = "DELETE FROM `group` WHERE group_id = ?;"
                data = (group_id,)
                cursor.execute(statement, data)
                if (cursor.rowcount > 0):
                    break
                print("Invalid group id. Please try again.")
            conn.commit()

            print("\nSuccessfully deleted group from the database")

        except db.Error as e:
            print(f"\nError deleting group from the database: {e}")
            conn.rollback()

        print("===========================================\n")

    else:
        print("Group table is empty\n")

    return None


def searchGroup(cursor: db.Cursor, conn: db.Connection) -> None:

    print("===========================================")
    print("SEARCH FOR A PARTICULAR GROUP")

    try:
        while True:
            group_id = int(input("Enter the id of the group to search: "))

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

                break

    except db.Error as e:
        print(f"\nError retrieving group from the database: {e}")

    print("===========================================\n")

    return None


def updateGroup(cursor: db.Cursor, conn: db.Connection) -> None:

    print("===========================================")
    print("\nEDIT DETAILS OF A PARTICULAR GROUP")

    while True:
        try:
            group_id_update = int(
                input("Enter the id of the group to update: "))
        except ValueError as e:
            print(f"Error: {e}\n")
        else:
            break

    try:
        statement = "SELECT * FROM `group` WHERE group_id = ?;"
        data = (group_id_update,)
        cursor.execute(statement, data)

        row = cursor.fetchone()

        if row is not None:
            group_id_print = row[0]
            group_name_print = row[1]
            group_balance_print = row[2]
            num_of_members_print = row[3]
            print("Current Detail of Group: ")
            print(
                f"Id: {group_id_print} | Name: {group_name_print} | Balance: {group_balance_print} | Number of members: {num_of_members_print}\n")

            while True:
                try:
                    group_name = get_string_input("Enter new group name: ")

                except ValueError as e:
                    print(f"Error: {e}\n")

                else:

                    break

            try:
                statement = "UPDATE `group` SET group_name = ? WHERE group_id = ?;"

                data = (group_name, group_id_update)
                cursor.execute(statement, data)
                conn.commit()
                print("\nSuccessfully updating of group in the database")

            except db.Error as e:
                print(f"\nError updating group in the database: {e}")
                conn.rollback()

    except db.Error as e:
        print(f"\nError retrieving group from the database: {e}")

    print("===========================================\n")

    return None


def getGroups(cursor: db.Cursor, conn: db.Connection) -> int:

    print("===========================================")
    print("GROUPS IN THE DATABASE")

    try:
        statement = "SELECT group_id, group_name FROM `group`;"
        cursor.execute(statement)

        # iterate over the users
        for i, row in enumerate(cursor):
            group_id = row[0]
            group_name = row[1]

            print(f"Id: {group_id} | Name: {group_name}")
            i = i + 1

    except db.Error as e:
        print(f"Error retrieving users from the database: {e}")

    return i


def addFriendToGroup(cursor: db.Cursor, conn: db.Connection, group_id) -> None:

    while True:
        try:
            while True:
                friendToAdd = get_int_input("Enter user id to add to group: ")

                if friendToAdd == 1:
                    print("You cannot add yourself to the group\n")
                    continue

                else:
                    try:
                        statement = "INSERT INTO is_part_of(user_id, group_id) VALUES(?, ?);"
                        data = (friendToAdd, group_id)
                        cursor.execute(statement, data)

                        statement = "UPDATE `group` SET num_of_members = num_of_members + 1 WHERE group_id = ?;"
                        data = (group_id,)
                        cursor.execute(statement, data)
                        conn.commit()

                        anotherFriend = input(
                            "\nDo you want to add another friend to the group? [y/n]: ")

                        if anotherFriend.lower() == "n":
                            break

                        elif anotherFriend.lower() == "y":
                            continue

                        else:
                            print("Invalid input.")
                            break

                    except db.Error as e:
                        print(f"Error retrieving users from the database: {e}")

        except ValueError as e:
            print(f"Error: {e}\n")

        else:
            break

    return None


def get_string_input(prompt: str) -> str:
    while 1:
        try:
            text = str(input(prompt).strip()).strip()
            if text == "":
                raise ValueError
            if len(text) > 20:
                raise ValueError
            return text
        except ValueError:
            print("Invalid input. Try again.")


def get_int_input(prompt: str) -> int:
    while True:
        try:
            num = int(input(prompt).strip())
            return num
        except ValueError:
            print("Invalid input. Please try again.")


def get_float_input(prompt: str) -> int:
    while True:
        try:
            num = float(input(prompt).strip())

            if num < 0:
                raise ValueError
            if num > 999999.99:
                raise ValueError
            return num
        except ValueError:
            print("Invalid input. Please try again.")


def addUser(cursor: db.Cursor, conn: db.Connection) -> None:

    try:
        statement = "INSERT INTO user(username, balance) VALUES('Danie', 0);"
        cursor.execute(statement)
        conn.commit()

        print("\nSuccessfully added group to the database")

    except db.Error as e:
        print(f"\nError adding group to the database: {e}")
        conn.rollback()

    return None

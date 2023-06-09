import mariadb as db
from tabulate import tabulate


def add_group(cursor: db.Cursor, conn: db.Connection) -> None:

    group_name = get_string_input("Enter the group name: ")

    try:
        cursor.execute(
            "INSERT INTO `group`(group_name) VALUES(?);", (group_name,))
        conn.commit()

        cursor.execute(
            "SELECT group_id FROM `group` WHERE group_name = ?;", (group_name,))
        group_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO is_part_of(user_id, group_id) VALUES(1, ?);", (group_id,))
        add_friend_to_group(cursor, conn, group_id)

        print("\nSuccessfully added group to the database")

    except db.Error as e:
        print(f"\nError adding group to the database: {e}")
        conn.rollback()

    return None


def delete_group(cursor: db.Cursor, conn: db.Connection) -> None:

    try:
        cursor.execute("SELECT * FROM `group`;")
        groups = cursor.fetchall()
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    if len(groups) <= 0:
        return None

    else:
        print_groups(groups)

        group_id = get_int_input("Enter the ID of the group to delete: ")

        try:
            cursor.execute(
                "DELETE FROM `group` WHERE group_id = ?;", (group_id,))
            conn.commit()
            print(f"Deleted {cursor.rowcount} group.")
        except db.Error as e:
            print(f"Error deleting group: {e}")

        return None


def search_group(cursor: db.Cursor) -> None:

    group_id = get_int_input("Enter group id: ")

    try:
        cursor.execute(
            "SELECT * FROM `group` WHERE group_id = ?;", (f"{group_id}",))
        groups = cursor.fetchall()

    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    print_groups(groups)

    return None


def update_group(cursor: db.Cursor, conn: db.Connection) -> None:

    try:
        cursor.execute("SELECT * FROM `group`;")
        groups = cursor.fetchall()
        print_groups(groups)

        group_id = get_int_input("Enter the ID of the group to update: ")

        # Update Username
        group_name = get_string_input("Enter new group name: ")
        cursor.execute(
            "UPDATE `group` SET group_name = ? WHERE group_id = ?;", (group_name, group_id))
        conn.commit()

        print(f"Updated {cursor.rowcount} group(s).")

    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    return None


def add_friend_to_group(cursor: db.Cursor, conn: db.Connection, group_id) -> None:

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


def print_groups(groups: list) -> None:
    print("=====================================")
    print("\t\tGroups")
    print("=====================================")
    print(tabulate(groups, headers=[
          "ID", "Group name", "Group Balance", "Number of Members"], tablefmt="rounded_grid"))
    print("=====================================")
    return None

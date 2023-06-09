import mariadb as db
from tabulate import tabulate
import modules.friend as friend


# Add a group to the database
def add_group(cursor: db.Cursor, conn: db.Connection) -> None:

    group_name = get_string_input("Enter the group name: ")

    try:
        # Set the name of the group
        cursor.execute(
            "INSERT INTO `group`(group_name) VALUES(?);", (group_name,))

        # Print all the friends in the database
        cursor.execute("SELECT * FROM user WHERE user.user_id != 1;")
        friends = cursor.fetchall()
        friend.print_users(friends)

        # Retrieve the group_id of the group that was just added
        cursor.execute(
            "SELECT group_id FROM `group` WHERE group_name = ?;", (group_name,))
        group_id = cursor.fetchone()[0]

        # Add the user to the group
        cursor.execute(
            "INSERT INTO is_part_of(user_id, group_id) VALUES(1, ?);", (group_id,))
        add_friend_to_group(cursor, conn, group_id)

        # Update the number of members in the group
        cursor.execute(
            "UPDATE `group` SET num_of_members = num_of_members + 1 WHERE group_id = ?;", (group_id,))
        conn.commit()

        print("\nSuccessfully added group to the database")

    # If there is an error, rollback the changes
    except db.Error as e:
        print(f"\nError adding group to the database: {e}")
        conn.rollback()

    return None


# Delete a group from the database
def delete_group(cursor: db.Cursor, conn: db.Connection) -> None:

    try:
        # Fetch all the groups in the database
        cursor.execute("SELECT * FROM `group`;")
        groups = cursor.fetchall()

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    # If there are no groups in the database, return None
    if len(groups) <= 0:
        print("There are no groups in the database.")
        return None

    else:
        # Print all the groups in the database
        print_groups(groups)

        # Get the group_id of the group to delete
        group_id = get_int_input("Enter the ID of the group to delete: ")

        try:
            # Delete the group from the database
            cursor.execute(
                "DELETE FROM `group` WHERE group_id = ?;", (group_id,))
            conn.commit()
            print(f"Deleted {cursor.rowcount} group.")

        # If there is an error, prompts the error
        except db.Error as e:
            print(f"Error deleting group from the database: {e}")

        return None


# Print all the groups in the database
def search_group(cursor: db.Cursor) -> None:

    # Get the group_id of the group to search
    group_id = get_int_input("Enter group id: ")

    try:
        # Fetch the group from the database
        cursor.execute(
            "SELECT * FROM `group` WHERE group_id = ?;", (f"{group_id}",))
        groups = cursor.fetchall()

        # If there are no groups in the database, return None
        if len(groups) <= 0:
            print("There are no groups in the database.")
            return None

        # Print the searched group
        print_groups(groups)

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    return None


# Update a group in the database
def update_group(cursor: db.Cursor, conn: db.Connection) -> None:

    try:
        # Print all the groups in the database
        cursor.execute("SELECT * FROM `group`;")
        groups = cursor.fetchall()

        # If there are no groups in the database, return None
        if len(groups) <= 0:
            print("There are no groups in the database.")
            return None

        print_groups(groups)

        # Get the group_id of the group to update
        group_id = get_int_input("Enter the ID of the group to update: ")

        # Update group name
        group_name = get_string_input("Enter new group name: ")
        cursor.execute(
            "UPDATE `group` SET group_name = ? WHERE group_id = ?;", (group_name, group_id))
        conn.commit()

        print(f"Updated {cursor.rowcount} group(s).")

    # If there is an error, prompts the error
    except db.Error as e:
        print(f"Error updating group: {e}")
        return None

    return None


# Add a friend to a group
def add_friend_to_group(cursor: db.Cursor, conn: db.Connection, group_id) -> None:

    while True:
        # Ask for the user id to add to the group
        friendToAdd = get_int_input("Enter user id to add to group: ")

        # Make sure that user doens't add themselves to the group
        if friendToAdd == 1:
            print("You cannot add yourself to the group\n")
            continue

        else:
            try:
                # Add a friend to the group and update the number of members in the group
                cursor.execute(
                    "INSERT INTO is_part_of(user_id, group_id) VALUES(?, ?);", (friendToAdd, group_id))
                cursor.execute(
                    "UPDATE `group` SET num_of_members = num_of_members + 1 WHERE group_id = ?;", (group_id,))
                conn.commit()

                # Ask if the user wants to add another friend to the group
                anotherFriend = input(
                    "\nDo you want to add another friend to the group? [y/n]: ")

                # If the user doesn't want to add another friend, break out of the loop
                if anotherFriend.lower() == "n":
                    return None

                # If the user wants to add another friend, continue the loop
                elif anotherFriend.lower() == "y":
                    continue

                # If the user enters an invalid input, break out of the loop
                else:
                    print("Invalid input.")
                    break

            # If there is an error, prompts the error
            except db.Error as e:
                print(f"Error adding user to the group: {e}")

    return None


# String input validation
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


# Int input validation
def get_int_input(prompt: str) -> int:
    while True:
        try:
            num = int(input(prompt).strip())
            return num
        except ValueError:
            print("Invalid input. Please try again.")


# Float input validation
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


# Print the groups in the database
def print_groups(groups: list) -> None:
    print("=====================================")
    print("\t\tGroups")
    print("=====================================")
    print(tabulate(groups, headers=[
          "ID", "Group name", "Group Balance", "Number of Members"], tablefmt="rounded_grid"))
    print("=====================================")
    return None

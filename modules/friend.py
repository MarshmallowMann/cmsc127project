import mariadb as db
from tabulate import tabulate


def addFriend(cursor: db.Cursor, connection: db.Connection) -> None:
    username = get_string_input("Enter username: ")
    beginBalance = get_float_input("Enter beginning balance: ")
    try:
        cursor.execute("INSERT INTO user (username, balance) VALUES (?, ?);",
                       (username, beginBalance))
        connection.commit()
        print("Friend added successfully.")
    except db.Error as e:
        print(f"Error adding friend: {e}")
    return None


def deleteFriend(cursor: db.Cursor, connection: db.Connection) -> None:
    # List all user
    try:
        cursor.execute("SELECT * FROM user WHERE user.user_id != 1;")
        friends = cursor.fetchall()
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    # Ask the user which user to delete
    print_users(friends)

    while True:
        toDelete = get_int_input("Enter the ID of the friend to delete: ")
        if toDelete == 1:
            print("Cannot delete the default user.")
        else:
            break

    # Check

    # Delete the user
    try:
        cursor.execute(
            "DELETE FROM user WHERE user_id = ? AND user_id != 1;", (toDelete,))
        # connection.commit()
        print(f"Deleted {cursor.rowcount} friend(s).")
    except db.Error as e:
        print(f"Error deleting friend: {e}")

    return None


def searchFriend(cursor: db.Cursor, connection: db.Connection) -> None:
    # Search for a user using the like operator with the username
    username = get_string_input("Enter username: ")

    try:
        cursor.execute(
            "SELECT * FROM user WHERE username LIKE ?;", (f"%{username}%",))
        friends = cursor.fetchall()
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    print_users(friends)

    return None


def updateFriend(cursor: db.Cursor, connection: db.Connection) -> None:
    try:
        cursor.execute("SELECT * FROM user WHERE user.user_id != 1;")
        friends = cursor.fetchall()
        print_users(friends)

        while 1:
            toUpdate = get_int_input("Enter the ID of the friend to update: ")
            if toUpdate != 1:
                break
            print("Cannot update the default user.")

        # Update Username
        username = get_string_input("Enter new username: ")
        cursor.execute(
            "UPDATE user SET username = ? WHERE user_id = ?;", (username, toUpdate))
        connection.commit()

        print(f"Updated {cursor.rowcount} friend(s).")

    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None
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


def print_users(friends: list) -> None:
    # Convert array of tuples to array of lists
    # friends = [list(friend) for friend in friends]
    print("=====================================")
    print("\t\tFriends")
    print("=====================================")
    print(tabulate(friends, headers=[
          "ID", "Username", "Balance"], tablefmt="rounded_grid"))
    print("=====================================")
    return None

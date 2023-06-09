import mariadb as db
from tabulate import tabulate


# Add a friend to the database
def addFriend(cursor: db.Cursor, connection: db.Connection) -> None:

    # Get the username and beginning balance from the user
    username = get_string_input("Enter username: ")
    beginBalance = get_float_input("Enter beginning balance: ")

    try:
        # Insert the user into the database
        cursor.execute("INSERT INTO user (username, balance) VALUES (?, ?);",
                       (username, beginBalance))
        connection.commit()
        print("Friend added successfully.")

    # If there is an error, prompt the error
    except db.Error as e:
        print(f"Error adding friend: {e}")

    return None


# Delete a friend from the database
def deleteFriend(cursor: db.Cursor, connection: db.Connection) -> None:

    try:
        # Fetch all the friends in the database
        cursor.execute("SELECT * FROM user WHERE user.user_id != 1;")
        friends = cursor.fetchall()

    # If there is an error, prompt the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    # Print all the friends in the database
    print_users(friends)

    while True:

        # Get the ID of the friend to delete
        toDelete = get_int_input("Enter the ID of the friend to delete: ")

        # If the user tries to delete the default user, prompt the error
        if toDelete == 1:
            print("Cannot delete the default user.")
        else:
            break

    try:
        # Delete the friend from the database
        cursor.execute(
            "DELETE FROM user WHERE user_id = ? AND user_id != 1;", (toDelete,))
        connection.commit()
        print(f"Deleted {cursor.rowcount} friend(s).")

    # If there is an error, prompt the error
    except db.Error as e:
        print(f"Error deleting friend: {e}")

    return None


# Search for a friend in the database
def searchFriend(cursor: db.Cursor, connection: db.Connection) -> None:

    # Search for a user using the like operator with the username
    username = get_string_input("Enter username: ")

    try:
        # Fetch friends with the provided username in the database
        cursor.execute(
            "SELECT * FROM user WHERE username LIKE ?;", (f"%{username}%",))
        friends = cursor.fetchall()

    # If there is an error, prompt the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

    # Print the searched friends in the database
    print_users(friends)

    return None


# Update a friend in the database
def updateFriend(cursor: db.Cursor, connection: db.Connection) -> None:

    try:
        # Fetch and print all the friends in the database
        cursor.execute("SELECT * FROM user WHERE user.user_id != 1;")
        friends = cursor.fetchall()
        print_users(friends)

        while 1:
            # Get the ID of the friend to update
            toUpdate = get_int_input("Enter the ID of the friend to update: ")

            # If the user tries to update the default user, prompt the error
            if toUpdate != 1:
                break
            print("Cannot update the default user.")

        # Get the new username from the user
        username = get_string_input("Enter new username: ")
        cursor.execute(
            "UPDATE user SET username = ? WHERE user_id = ?;", (username, toUpdate))
        connection.commit()

        print(f"Updated {cursor.rowcount} friend(s).")

    # If there is an error, prompt the error
    except db.Error as e:
        print(f"Error fetching data: {e}")
        return None

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


# Print the friends in the database
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

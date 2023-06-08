import mariadb as db


def addFriend(cursor: db.Cursor, connection: db.Connection) -> None:
    username = get_string_input("Enter username: ")
    beginBalance = get_float_input("Enter beginning balance: ")
    try:
        cursor.execute("INSERT INTO user (username, balance) VALUES (?, ?)",
                       (username, beginBalance))
        connection.commit()
        print("Friend added successfully.")
    except db.Error as e:
        print(f"Error adding friend: {e}")
    return None


def deleteFriend(cursor: db.Cursor, connection: db.Connection) -> None:
    # List all user

    return None


def searchFriend(cursor: db.Cursor, connection: db.Connection) -> None:
    return None


def updateFriend(cursor: db.Cursor, connection: db.Connection) -> None:
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

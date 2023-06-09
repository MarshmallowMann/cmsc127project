import mariadb as db
from datetime import date
from tabulate import tabulate


def addExpense(cursor: db.Cursor, conn: db.Connection) -> None:
    return None


def getUsers(cursor: db.Cursor) -> None:
    try:
        statement = "SELECT username FROM user WHERE user_id != 1"
        cursor.execute(statement)
        print("\n[Users]")
        # iterate over the users
        for i, row in enumerate(cursor):
            username = row[0]
            # start with the second user because the first user is the one using the app
            print(f"[{i+2}] {username}")
    except db.Error as e:
        print(f"Error retrieving users from the database: {e}")


def getUserCount(cursor: db.Cursor) -> int:
    statement = "SELECT COUNT(DISTINCT user_id) FROM user"
    cursor.execute(statement)
    user_count = cursor.fetchone()[0]
    return user_count


def get_user_is_lender():
    user_is_lender = None
    while user_is_lender not in [1, 2]:
        user_is_lender = input(
            "\nAre you a lender or a borrower?\n[1]Lender\n[2]Borrower\nChoice: ")
        if user_is_lender == '1':
            user_is_lender = 1  # user is a lender
        elif user_is_lender == '2':
            user_is_lender = 2  # user is a borrower
        else:
            print("\n[ERROR] Invalid Input. Please Choose 1 or 2.\n")
    return user_is_lender


def chooseFriend(user_count) -> int:
    chosen_friend = None
    # continue to ask user to input correct borrower number
    while chosen_friend is None or not (2 <= chosen_friend <= user_count):
        try:
            chosen_friend = int(
                input("\nInput the number for the chosen borrower: "))
            if not (2 <= chosen_friend <= user_count):
                print("\nInvalid input. Please enter a valid number for the borrower.")
        except ValueError:
            print("\nInvalid input. Please enter a valid integer.\n")
    return chosen_friend


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


def addIsCreatedBy(cursor: db.Cursor, connection: db.Connection, transaction_id, user_id, group_id) -> None:
    try:
        # if group transaction
        statement = "INSERT INTO is_created_by(transaction_id, user_id, group_id) VALUES (%d, %d, %d)"
        data = (transaction_id, user_id, group_id)
        cursor.execute(statement, data)
        connection.commit()
        print("Successfully added is_created_by group transaction to the database.")
    except db.Error as e:
        print(
            f"Error adding is_created_by group transaction to the database: {e}")


def addIsMadeBy(cursor: db.Cursor, transaction_id, user_id) -> None:
    try:
        # if user single transaction
        statement = "INSERT INTO is_made_by(transaction_id, user_id) VALUES (%d, %d)"
        data = (transaction_id, user_id)
        cursor.execute(statement, data)
        print("Successfully added is_made_by single transaction to the database.")
    except db.Error as e:
        print(
            f"Error adding is_made_by single transaction to the database: {e}")


def getTransactionCount(cursor: db.Cursor) -> int:
    statement = "SELECT COUNT(DISTINCT transaction_id) FROM transaction"
    cursor.execute(statement)
    transaction_count = cursor.fetchone()[0]
    print("Transaction Count is ", transaction_count)
    return transaction_count


def userLendTransaction(cursor: db.Cursor, transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id) -> None:
    try:
        statement = "INSERT INTO transaction(transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id) VALUES (%d, %s,%s,%d,%d,%d,%d)"
        data = (transaction_amount, transaction_date,
                transaction_type, isLoan, lender, isPaid, user_id)
        cursor.execute(statement, data)
        print("[USER LEND TRANSACTION] Successfully added transaction to the database")
    except db.Error as e:
        print(
            f"[USER LEND TRANSACTION] Error adding transaction to the database: {e}")


def updateUserBalance(cursor: db.Cursor, user_id, transaction_amount) -> None:
    try:
        statement = "UPDATE user SET balance = balance + %d WHERE user_id = %d"
        data = (transaction_amount, user_id)
        cursor.execute(statement, data)
        print("[USER UPDATE BALANCE] Successfully updated user (borrower) balance")
    except db.Error as e:
        print(
            f"[USER UPDATE BALANCE] Error updating user (borrower) balance: {e}")


def askAmount() -> float:
    transaction_amount = None
    while transaction_amount is None or not (1 <= transaction_amount <= 999999.99):
        try:
            transaction_amount = float(input("\nInput transaction amount: "))
            if not (1 <= transaction_amount <= 999999.99):
                print("\nInvalid input. Please enter a value between 1 and 999999.99.\n")
        except ValueError:
            print("\nInvalid input. Please enter a valid number.\n")
    return transaction_amount


def getDate() -> str:
    today = date.today()
    transaction_date = today.strftime("%Y-%m-%d")
    return transaction_date


def askTransactionType() -> str:
    transaction_type = None
    while transaction_type not in ['1', '2']:  # 1 = loan, 2 = settlement
        transaction_type = input(
            "\nChoose Group Transaction Type:\n[1] Loan\n[2] Settlement\nChoice: ")
        if transaction_type == '1':  # loan
            transaction_type = 'loan'
        elif transaction_type == '2':  # settlement
            transaction_type = 'settlement'
        else:
            print("\n[ERROR] Invalid Input. Please Choose 1 or 2.\n")
    return transaction_type


def createGroupTransaction(cursor: db.Cursor) -> None:
    transaction_amount = askAmount()
    transaction_date = getDate()
    transaction_type = askTransactionType()
    if transaction_type == 'loan':
        isLoan = 1
        userIsLender = get_user_is_lender()
        if userIsLender == 1:  # user is a lender
            lender = 1
            # ask user to select a borrower
            print("Choose a borrower:")
            # get the user count using the getUsers() function
            getUsers(cursor)
            # get the chosen friend using the chooseFriend() function
            user_id = chooseFriend(getUserCount(cursor))


# [] Group Loan
# INSERT INTO transaction(transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, isGroupLoan, user_id, group_id)
# VALUES(100, '2020-11-12', 'loan', 1, 1, 0, 1, 1, 1);

# [] Group Settlement
# - User Loan

def addExpense(cursor: db.Cursor, connection: db.Connection) -> None:
    try:
        transaction_creator = None
        while transaction_creator not in ['1', '2']:  # 1 = user, 2 = group
            transaction_creator = input(
                "\nChoose Transaction Creator:\n[1] User\n[2] Group\nChoice: ")
            if transaction_creator == '1':  # user transaction
                # input transaction amount
                transaction_amount = askAmount()
                transaction_date = getDate()

                transaction_type_choice = None  # Initialize transaction_type with None
                while transaction_type_choice not in ['1', '2']:
                    transaction_type_choice = input(
                        "Choose transaction type:\n[1]Loan\n[2]Settlement\nChoice: ")

                    # LOAN
                    if transaction_type_choice == '1':
                        transaction_type = "loan"  # transaction type is a loan
                        isLoan = 1  # set to true
                        isPaid = 0  # set to false

                        # ask user if borrower or lender
                        userIsLender = get_user_is_lender()

                        if userIsLender == 1:  # user is a lender
                            lender = 1
                            # ask user to select a borrower
                            print("Choose a borrower:")
                            # get the user count using the getUsers() function
                            getUsers(cursor)
                            # get the chosen friend using the chooseFriend() function
                            user_id = chooseFriend(getUserCount(cursor))
                            userLendTransaction(
                                cursor, transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id)
                            transaction_id = cursor.lastrowid
                            # is_made_by to create connection between transaction and user
                            addIsMadeBy(cursor, transaction_id, user_id)
                            # update user balance of borrower
                            updateUserBalance(
                                cursor, user_id, transaction_amount)

                        else:  # user is a borrower
                            # user (with user_id 1) is the borrower
                            user_id = 1
                            isLoan = 1
                            # ask user to select a lender
                            print("Choose a lender:")
                            # get the user count using the getUsers() function
                            getUsers(cursor)
                            # get the chosen friend using the chooseFriend() function
                            lender = chooseFriend(getUserCount(cursor))
                            userLendTransaction(
                                cursor, transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id)
                            transaction_id = cursor.lastrowid
                            # is_made_by to create connection between transaction and user
                            addIsMadeBy(cursor, transaction_id, user_id)
                            # update user balance of borrower
                            updateUserBalance(
                                cursor, user_id, transaction_amount)

            else:  # group transaction (transaction_creator == 2)
                createGroupTransaction(cursor)

        # create a sample loan transaction with a lender and a borrower(user is the borrower)
        # ask if user is the borrower or the lender


#         INSERT INTO transaction(transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id)
# VALUES(100, '2020-11-11', 'loan', 1, 1, 0, 2);

        # statement = "INSERT INTO employees (first_name, last_name) VALUES (%s, %s)"
        # data = (first_name, last_name)
        # cursor.execute(statement, data)

        connection.commit()
        print("[END] Successfully added transaction to the database")
    except db.Error as e:
        print(f"Error adding transaction to the database: {e}")
    return None


def deleteExpense(cursor: db.Cursor) -> None:
    return None


def searchExpense(cursor: db.Cursor) -> None:
    return None


def updateExpense(cursor: db.Cursor, connection: db.Connection) -> None:
    print("""
    [1] Individual Settlement
    [2] Group Settlement
          """)

    choice = get_int_input("Enter your choice: ")

    if choice == 1:
        individualSettlement(cursor, connection, "settlement")
    elif choice == 2:
        groupSettlement(cursor, connection, "settlement")
    else:
        print("Invalid input. Please try again.")

    return None


def print_loans(loans: list) -> None:
    # SELECT user_id, transaction_id, transaction_amount, transaction_date, lender
    print("=====================================")
    print("\t\tLoans")
    print(tabulate(loans, headers=["User Id", "Transaction Id",
          "Transaction Amount", "Transaction Date", "Lender"], tablefmt="rounded_grid"))
    print("=====================================")
    return None


def print_groups(groups: list) -> None:
    # SELECT user_id, transaction_id, transaction_amount, transaction_date, lender
    print("=====================================")
    print("\t\tLoans")
    print(tabulate(groups, headers=[
          "Group Id", "Transaction Id"], tablefmt="rounded_grid"))
    print("=====================================")
    return None


def individualSettlement(cursor: db.Cursor, connection: db.Connection, transaction_type: str) -> None:
    transaction_type = "settlement"
    try:
        cursor.execute(
            "SELECT user_id, transaction_id, transaction_amount, transaction_date, lender  FROM transaction  WHERE isLoan = 1 AND isPaid = 0 AND user_id = 1;")
        print_loans(cursor.fetchall())

        toSettle = get_int_input(
            "Enter the transaction_id of the loan to settle: ")

        cursor.execute(
            "SELECT * FROM transaction WHERE transaction_id = ? AND isLoan = 1 AND isPaid = 0 AND user_id = 1;", (toSettle,))
        loan = cursor.fetchone()
        if loan is None:
            print("Invalid transaction_id.")
            return None

        # Create a new Settlement transaction
        try:
            cursor.execute("INSERT INTO transaction (transaction_amount, transaction_date, transaction_type, isSettlement, settledLoan, user_id) VALUES (?, ?, ?, ?, ?, ?);",
                           (loan[1], date.today(), transaction_type, 1, loan[0], 1))
        except db.Error as e:
            print(f"Error adding transaction to the database: {e}")
            return None
        # Mark the loan transaction as paid
        try:
            cursor.execute(
                "UPDATE transaction SET isPaid = 1 WHERE transaction_id = ?;", (toSettle,))
        except db.Error as e:
            print(f"Error updating transaction: {e}")
            return None
        # Update the balance of the borrower
        balance = loan[1] * -1

        try:
            cursor.execute(
                "UPDATE user SET balance = balance + ? WHERE user_id = ?;", (balance, 1))
        except db.Error as e:
            print(f"Error updating user balance: {e}")
            return None

        # Commit
        connection.commit()
        print("Successfully settled the loan.")
        return None

    except db.Error as e:
        print(f"Error retrieving loans from the database: {e}")
        return None


def groupSettlement(cursor: db.Cursor, connection: db.Connection, transaction_type: str) -> None:
    transaction_type = "settlement"
    try:
        # List all the groups with outstanding balance
        cursor.execute("SELECT is_created_by.group_id, group_name FROM is_created_by JOIN `group` ON is_created_by.group_id = `group`.group_id JOIN transaction t on is_created_by.transaction_id = t.transaction_id WHERE isLoan = 1 AND isPaid = 0 AND t.user_id = 1 AND isGroupLoan = 1;")
        groups = cursor.fetchall()

        print_groups(groups)

        group_id = get_int_input("Enter the group_id of the group to settle: ")

        # List all the loans in the group
        cursor.execute("SELECT user_id, transaction_id, transaction_amount, transaction_date, lender  FROM transaction  WHERE isLoan = 1 AND isPaid = 0 AND user_id = 1 AND isGroupLoan = 1 AND group_id = ?;", (group_id,))
        print_loans(cursor.fetchall())

        toSettle = get_int_input(
            "Enter the transaction_id of the loan to settle: ")

        cursor.execute(
            "SELECT * FROM transaction WHERE transaction_id = ? AND isLoan = 1 AND isPaid = 0 AND user_id = 1 AND isGroupLoan = 1 AND group_id = ?;", (toSettle, group_id))
        loan = cursor.fetchone()
        if loan is None:
            print("Invalid transaction_id.")
            return None

        # Create a new Settlement transaction
        try:
            cursor.execute("INSERT INTO transaction (transaction_amount, transaction_date, transaction_type, isSettlement, settledLoan, user_id, group_id) VALUES (?, ?, ?, ?, ?, ?);",
                           (loan[1], date.today(), transaction_type, 1, loan[0], 1, loan[6]))
        except db.Error as e:
            print(f"Error adding transaction to the database: {e}")
            return None
        # Mark the loan transaction as paid
        try:
            cursor.execute(
                "UPDATE transaction SET isPaid = 1 WHERE transaction_id = ?;", (toSettle,))
        except db.Error as e:
            print(f"Error updating transaction: {e}")
            return None
        # Update the balance of the borrower
        balance = loan[1] * -1

        # Update the balance of the group members
        try:
            cursor.execute(
                "UPDATE user SET balance = balance + ? WHERE user_id IN (SELECT DISTINCT group_id FROM is_part_of WHERE group_id = ?);", (balance, loan[6]))
        except db.Error as e:
            print(f"Error updating group balance: {e}")
            return None

        # Commit
        connection.commit()
        print("Successfully settled the loan.")
        return None

    except db.Error as e:
        print(f"Error retrieving loans from the database: {e}")
        return None

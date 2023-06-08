import mariadb as db
from datetime import date

def addExpense(cursor: db.Cursor, conn: db.Connection) -> None:
    return None

def getUsers(cursor: db.Cursor) -> None:
    try:
        statement = "SELECT username FROM user"
        cursor.execute(statement)
        print("\n[Users]")
        # iterate over the users
        for i, row in enumerate(cursor):
            username = row[0]
            print(f"[{i+2}] {username}") # start with the second user because the first user is the one using the app
    except db.Error as e:
        print(f"Error retrieving users from the database: {e}")

def getUserCount(cursor: db.Cursor) -> int:
    statement = "SELECT COUNT(DISTINCT user_id) FROM user"
    cursor.execute(statement)
    user_count = cursor.fetchone()[0]
    return user_count

def get_user_type():
    user_is_lender = None
    while user_is_lender not in [1, 2]:
        user_is_lender = input("Are you a lender or a borrower?\n[1]Lender\n[2]Borrower\nChoice: ")
        if user_is_lender == '1':
            user_is_lender = 1  # user is a lender
        elif user_is_lender == '2':
            user_is_lender = 2  # user is a borrower
        else:
            print("\n[ERROR] Invalid Input. Please Choose 1 or 2.\n")
    return user_is_lender

def chooseFriend(user_count) -> str:
    chosen_friend = None
    while chosen_friend is None or not (2 <= chosen_friend <= user_count): # continue to ask user to input correct borrower number 
        try:
            chosen_friend = int(input("\nInput the number for the chosen borrower: "))
            if not (2 <= chosen_friend <= user_count):
                print("\nInvalid input. Please enter a valid number for the borrower.\n")
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
        statement = "INSERT INTO is_created_by (transaction_id, user_id, group_id) VALUES (%s, %s, %s)"
        data = (transaction_id, user_id, group_id)
        cursor.execute(statement, data)
        connection.commit()
        print("Successfully added is_created_by group transaction to the database.")
    except db.Error as e:
        print(f"Error adding is_created_by group transaction to the database: {e}")

def addIsMadeBy(cursor: db.Cursor, connection: db.Connection, transaction_id, user_id) -> None:
    try:
        # if user single transaction
        statement = "INSERT INTO is_made_by(transaction_id, user_id) VALUES (%s, %s)"
        data = (transaction_id, user_id)
        cursor.execute(statement, data)
        connection.commit()
        print("Successfully added is_made_by single transaction to the database.")
    except db.Error as e:
        print(f"Error adding is_made_by single transaction to the database: {e}")


def addExpense(cursor: db.Cursor, connection: db.Connection) -> None:
    try:
        transaction_creator = None
        while transaction_creator not in [1,2]: # 1 = user, 2 = group
            transaction_creator = input("Choose Transaction Creator:\n[1] User\n[2] Group\nChoice: ")
            if transaction_creator=='1': # user transaction
                # is_made_by 
                # input transaction amount
                transaction_amount = None
                while transaction_amount is None or not (1 <= transaction_amount <= 999999.99):
                    try:
                        transaction_amount = float(input("Input transaction amount: "))
                        if not (1 <= transaction_amount <= 999999.99):
                            print("\nInvalid input. Please enter a value between 1 and 999999.99.\n")
                    except ValueError:
                        print("\nInvalid input. Please enter a valid number.\n")

                today = date.today()
                transaction_date = today.strftime("%Y-%m-%d")
                
                transaction_type_choice = None  # Initialize transaction_type with None

                while transaction_type_choice not in [1, 2]:
                    transaction_type_choice = input("Choose transaction type:\n[1]Loan\n[2]Settlement\nChoice: ")

                    # LOAN
                    if transaction_type_choice == '1':
                        transaction_type = "loan" # transaction type is a loan
                        isLoan = 1 # set to true
                        isPaid = 0 # set to false
                        
                        # ask user if borrower or lender
                        userIsLender = get_user_type()
                                
                                
                        if userIsLender==1: # user is a lender
                            lender = 1
                            # ask user to select a borrower
                            print("Choose a borrower:")
                            getUsers(cursor)  # get the user count using the getUsers() function
                            chosen_friend = chooseFriend(getUserCount(cursor))  # get the chosen friend using the chooseFriend() function
                                    
                                    
                        else: # user is a borrower
                            user_id = 1 # user (with user_id 1) is the borrower
                            isLoan = 1
                            # ask user to select a lender
                            print("Choose a lender:")
                            user_count = getUsers(cursor)  # get the user count using the getUsers() function
                            chosen_friend = chooseFriend(getUserCount(cursor))  # get the chosen friend using the chooseFriend() function
                    
                    
                    # SETTLEMENT
                    elif transaction_type_choice == '2':
                        transaction_type = "settlement"
                    else:
                        print("\n[ERROR] Invalid Input. Please Choose 1 or 2.\n")

        # create a sample loan transaction with a lender and a borrower(user is the borrower)
        # ask if user is the borrower or the lender

        
        

        # print("transaction_amount: \n", transaction_amount)
        # print("transaction_date: \n", transaction_date)
        # print("transaction_type: \n", transaction_type)
        # print("userIsLender: \n", userIsLender)

        # else # user is a borrower
        
        
        # create a sample group loan transaction with a lender
        
        
        # create a sample settlement transaction with a lender and a borrower
        
        
        
        
        
        
#         INSERT INTO transaction(transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id) 
# VALUES(100, '2020-11-11', 'loan', 1, 1, 0, 2);

        statement = "INSERT INTO employees (first_name, last_name) VALUES (%s, %s)"
        data = (first_name, last_name)
        cursor.execute(statement, data)
        
        
        connection.commit()
        print("Successfully added entry to the database")
    except db.Error as e:
        print(f"Error adding entry to the database: {e}")
    return None

def deleteExpense(cursor: db.Cursor) -> None:
    return None


def searchExpense(cursor: db.Cursor) -> None:
    return None


def updateExpense(cursor: db.Cursor) -> None:
    return None
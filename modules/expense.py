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
            print(f"[{i+2}] {username}") # start with the second user because the first user is the one using the app
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
        user_is_lender = input("\nAre you a lender or a borrower?\n[1]Lender\n[2]Borrower\nChoice: ")
        if user_is_lender == '1':
            user_is_lender = 1  # user is a lender
        elif user_is_lender == '2':
            user_is_lender = 2  # user is a borrower
        else:
            print("\n[ERROR] Invalid Input. Please Choose 1 or 2.\n")
    return user_is_lender

def chooseFriend(user_count) -> int:
    chosen_friend = None
    while chosen_friend is None or not (2 <= chosen_friend <= user_count): # continue to ask user to input correct borrower number 
        try:
            chosen_friend = int(input("\nInput the number for the chosen borrower: "))
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
        print(f"Error adding is_created_by group transaction to the database: {e}")

def addIsMadeBy(cursor: db.Cursor, transaction_id, user_id) -> None:
    try:
        # if user single transaction
        statement = "INSERT INTO is_made_by(transaction_id, user_id) VALUES (%d, %d)"
        data = (transaction_id, user_id)
        cursor.execute(statement, data)
        print("Successfully added is_made_by single transaction to the database.")
    except db.Error as e:
        print(f"Error adding is_made_by single transaction to the database: {e}")

def getTransactionCount(cursor: db.Cursor) -> int:
    statement = "SELECT COUNT(DISTINCT transaction_id) FROM transaction"
    cursor.execute(statement)
    transaction_count = cursor.fetchone()[0]
    print("Transaction Count is ", transaction_count)
    return transaction_count

def userLendTransaction(cursor: db.Cursor, transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id) -> None:
    try:
        statement = "INSERT INTO transaction(transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id) VALUES (%d, %s,%s,%d,%d,%d,%d)"
        data = (transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id)
        cursor.execute(statement, data)
        print("[USER LEND TRANSACTION] Successfully added transaction to the database")
    except db.Error as e:
        print(f"[USER LEND TRANSACTION] Error adding transaction to the database: {e}")


def updateUserBalance(cursor: db.Cursor, user_id, transaction_amount) -> None:
    try:
        statement = "UPDATE user SET balance = balance + %d WHERE user_id = %d"
        data = (transaction_amount, user_id)
        cursor.execute(statement, data)
        print("[USER UPDATE BALANCE] Successfully updated user (borrower) balance")
    except db.Error as e:
        print(f"[USER UPDATE BALANCE] Error updating user (borrower) balance: {e}")
         
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
    while transaction_type not in ['1','2']: # 1 = loan, 2 = settlement
        transaction_type = input("\nChoose Group Transaction Type:\n[1] Loan\n[2] Settlement\nChoice: ")
        if transaction_type=='1': # loan
            transaction_type = 'loan'
        elif transaction_type=='2': # settlement
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
        if userIsLender==1: # user is a lender
            lender = 1
            # ask user to select a borrower
            print("Choose a borrower:")
            getUsers(cursor)  # get the user count using the getUsers() function
            user_id = chooseFriend(getUserCount(cursor))  # get the chosen friend using the chooseFriend() function
            
            
            
        else: # user is a borrower
            
            
            

    else: # transaction_type == 'settlement'
        
    
# [] Group Loan
# INSERT INTO transaction(transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, isGroupLoan, user_id, group_id)
# VALUES(100, '2020-11-12', 'loan', 1, 1, 0, 1, 1, 1);

# [] Group Settlement
# - User Loan

def addExpense(cursor: db.Cursor, connection: db.Connection) -> None:
    try:
        transaction_creator = None
        while transaction_creator not in ['1','2']: # 1 = user, 2 = group
            transaction_creator = input("\nChoose Transaction Creator:\n[1] User\n[2] Group\nChoice: ")
            if transaction_creator=='1': # user transaction
                # input transaction amount
                transaction_amount = askAmount()
                transaction_date = getDate()
                
                transaction_type_choice = None  # Initialize transaction_type with None
                while transaction_type_choice not in ['1', '2']:
                    transaction_type_choice = input("Choose transaction type:\n[1]Loan\n[2]Settlement\nChoice: ")

                    # LOAN
                    if transaction_type_choice == '1':
                        transaction_type = "loan" # transaction type is a loan
                        isLoan = 1 # set to true
                        isPaid = 0 # set to false
                    
                        # ask user if borrower or lender
                        userIsLender = get_user_is_lender()
                                    
                        if userIsLender==1: # user is a lender
                            lender = 1
                            # ask user to select a borrower
                            print("Choose a borrower:")
                            getUsers(cursor)  # get the user count using the getUsers() function
                            user_id = chooseFriend(getUserCount(cursor))  # get the chosen friend using the chooseFriend() function
                            userLendTransaction(cursor, transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id)
                            transaction_id = cursor.lastrowid
                            addIsMadeBy(cursor, transaction_id, user_id) # is_made_by to create connection between transaction and user 
                            updateUserBalance(cursor, user_id, transaction_amount) # update user balance of borrower
                            
                            
                        else: # user is a borrower
                            user_id = 1 # user (with user_id 1) is the borrower
                            isLoan = 1
                            # ask user to select a lender
                            print("Choose a lender:")
                            getUsers(cursor)  # get the user count using the getUsers() function
                            lender = chooseFriend(getUserCount(cursor))  # get the chosen friend using the chooseFriend() function
                            userLendTransaction(cursor, transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id)
                            transaction_id = cursor.lastrowid
                            addIsMadeBy(cursor, transaction_id, user_id) # is_made_by to create connection between transaction and user 
                            updateUserBalance(cursor, user_id, transaction_amount) # update user balance of borrower

                    # SETTLEMENT
                    elif transaction_type_choice == '2':
                        transaction_type = "settlement"
                        # Print all the transactions marked as loans and is not paid yet
                        print_loans(cursor.fetchall())
                        try:
                            cursor.execute(
                                "SELECT is_made_by.user_id, is_made_by.transaction_id, transaction_amount, transaction_date, lender  FROM transaction NATURAL JOIN is_made_by WHERE isLoan = 1 AND isPaid = 0 AND is_made_by.user_id = 1;");
                            
                        except db.Error as e:
                            print(f"Error retrieving loans from the database: {e}")
                            return None
                        
                        # User selects the loan that user will settle. 
                        # User will input the transaction_id of the loan that user will settle.
                        
                        # Settlement
                        # loan transaction is paid will be marked as true.
                        # user balance of the borrower will be updated (balance = balance - transaction_amount)
                        # user balance of the lender will be updated (balance = balance + transaction_amount)
                        
                        
                    else:
                        print("\n[ERROR] Invalid Input. Please Choose 1 or 2.\n")
            
            else: # group transaction (transaction_creator == 2)
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


def updateExpense(cursor: db.Cursor) -> None:
    return None


def print_loans(loans: list) -> None:
    print("=====================================")
    print("\t\tLoans")
    print(tabulate(loans, tablefmt="rounded_grid"))
    print("=====================================")
    return None
import mariadb as db
from datetime import date
from tabulate import tabulate

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
            
def addIsCreatedBy(cursor: db.Cursor, transaction_id, user_id, group_id) -> None:
    try:
        # if group transaction
        statement = "INSERT INTO is_created_by(transaction_id, user_id, group_id) VALUES (%d, %d, %d)"
        data = (transaction_id, user_id, group_id)
        cursor.execute(statement, data)
        print("[ADD IS_CREATED_BY] Successfully added is_created_by group transaction to the database.")
    except db.Error as e:
        print(f"Error adding is_created_by group transaction to the database: {e}")

def getTransactionCount(cursor: db.Cursor) -> int:
    statement = "SELECT COUNT(DISTINCT transaction_id) FROM transaction"
    cursor.execute(statement)
    transaction_count = cursor.fetchone()[0]
    print("Transaction Count is ", transaction_count)
    return transaction_count

def userLendTransaction(cursor: db.Cursor, transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id) -> None:
    try:
        statement = "INSERT INTO transaction(transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id) VALUES (%s, %s,%s,%s,%s,%s,%s)"
        data = (transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id)
        cursor.execute(statement, data)
        print("[USER LEND TRANSACTION] Successfully added transaction to the database")
    except db.Error as e:
        print(f"[USER LEND TRANSACTION] Error adding transaction to the database: {e}")


def updateUserBalance(cursor: db.Cursor, user_id, transaction_amount) -> None:
    try:
        statement = "UPDATE user SET balance = balance + %s WHERE user_id = %s"
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

def getGroups(cursor: db.Cursor) -> None:
    try:
        statement = "SELECT group_name FROM `group`"
        cursor.execute(statement)
        print("[GROUPS]")
        # iterate over the users
        for i, row in enumerate(cursor):
            groupname = row[0]
            print(f"[{i+1}] {groupname}") # show all groups 
    except db.Error as e:
        print(f"[GET ALL GROUPS] Error retrieving groups from the database: {e}")    
    
def setGroupID(cursor: db.Cursor) -> int:
# Check if there are any groups in the database
    cursor.execute("SELECT COUNT(*) FROM `group`")
    group_count = cursor.fetchone()[0]

    if group_count == 0:
        print("\nThere are no groups created yet.\n")
        return None # returns None if there are no groups created yet.
    
    group_id = None
    while group_id is None:
        try:
            group_id = int(input("\nChoice: "))
            statement = "SELECT group_id FROM `group` WHERE group_id = %d"
            data = (group_id,)
            cursor.execute(statement, data)
            if cursor.fetchone() is None:
                print("\nInvalid input. Please enter a valid group id.\n")
                group_id = None
        except ValueError:
            print("\nInvalid input. Please enter a valid integer.\n")
    return group_id
    
def chooseGroup(cursor: db.Cursor) -> int:
    print("\nChoose a group to transact with:")
    getGroups(cursor)
    group_id = setGroupID(cursor)
    return group_id

def getGroupMembers(cursor: db.Cursor, group_id, lender) -> list:
    try:
        statement = "SELECT user_id FROM is_part_of WHERE group_id = %d AND user_id != %d"
        data = (group_id,lender)
        cursor.execute(statement, data)
        members = []
        for row in cursor:
            members.append(row[0])
            
        print(f"[GET GROUP MEMBERS] Successfully retrieved group members from the database.")
        return members
    except db.Error as e:
        print(f"[GET GROUP MEMBERS] Error retrieving group members from the database: {e}")

def getMemberCount(cursor: db.Cursor, group_id: int) -> int:
    try:
        statement = "SELECT num_of_members FROM `group` WHERE group_id = %s"
        data = (group_id,)
        cursor.execute(statement, data)
        result = cursor.fetchone()
        num_of_members = result[0]
        return num_of_members
    except db.Error as e:
        print(f"Error retrieving member count from the database: {e}")
        
def updateMembersBalance(cursor: db.Cursor, members: list, dividedAmount: float) -> None:
    try:
        statement = "UPDATE user SET balance = balance + %s WHERE user_id = %s"
        for member in members:
            data = (dividedAmount, member)
            cursor.execute(statement, data)
        print("[USER UPDATE BALANCE] Successfully updated user (borrower) balance")
    except db.Error as e:
        print(f"[USER UPDATE BALANCE] Error updating user (borrower) balance: {e}")

def updateGroupBalance(cursor: db.Cursor, group_id: int, transaction_amount: float) -> None:
    try:
        statement = "UPDATE `group` SET group_balance = group_balance + %s WHERE group_id = %s"
        data = (transaction_amount, group_id)
        cursor.execute(statement, data)
        print("[GROUP UPDATE BALANCE] Successfully updated group balance")
    except db.Error as e:
        print(f"[GROUP UPDATE BALANCE] Error updating group balance: {e}")

# addGroupTransaction using this: # INSERT INTO transaction(transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, isGroupLoan, amountRemaining, dividedAmount, user_id, group_id)
def addLenderGroupTransaction(cursor: db.Cursor, transaction_amount: float, transaction_date: str, isPaid: int, isGroupLoan: int, amountRemaining: float, dividedAmount: float, user_id: int, group_id: int) -> None:
    try:
        statement = "INSERT INTO transaction(transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, isGroupLoan, amountRemaining, dividedAmount, user_id, group_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %d, %d)"
        data = (transaction_amount, transaction_date, "loan", 1, user_id, isPaid, isGroupLoan, amountRemaining, dividedAmount, user_id, group_id)
        cursor.execute(statement, data)
        print("[ADD LENDER GROUP TRANSACTION] Successfully added group transaction")
    except db.Error as e:
        print(f"[ADD LENDER GROUP TRANSACTION] Error adding group transaction: {e}")

def chooseLender(cursor: db.Cursor, group_id: int) -> int:
    try:
        # Retrieve the list of group members
        statement = "SELECT user_id, username FROM user WHERE user_id IN (SELECT user_id FROM is_part_of WHERE group_id = %s AND user_id!=1)"
        data = (group_id,)
        cursor.execute(statement, data)
        members = cursor.fetchall()

        # Display the list of group members to the user
        print("\n[LIST OF GROUP MEMBERS]")
        for member in members:
            user_id, username = member
            print(f"ID: [{user_id}] {username}")

        # Prompt the user to choose a lender
        lender_id = None
        while lender_id is None:
            lender_input = input("\nEnter the ID of the lender: ")
            try:
                lender_id = int(lender_input)
                if lender_id not in [member[0] for member in members]:
                    print("Invalid lender ID. Please choose a valid lender ID.")
                    lender_id = None
            except ValueError:
                print("Invalid input. Please enter a valid lender ID.")

        return lender_id

    except db.Error as e:
        print(f"[CHOOSE LENDER] Error retrieving group members from the database: {e}")

def addBorrowerGroupTransaction(cursor: db.Cursor, transaction_amount: float, transaction_date: str, isPaid: int, isGroupLoan: int, amountRemaining: float, dividedAmount: float, user_id: int, group_id: int) -> None:
    try:
        statement = "INSERT INTO transaction(transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, isGroupLoan, amountRemaining, dividedAmount, user_id, group_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %d, %d)"
        data = (transaction_amount, transaction_date, "loan", 1, user_id, isPaid, isGroupLoan, amountRemaining, dividedAmount, 1, group_id) # user_id equal to 1 or the user who created the group transaction
        cursor.execute(statement, data)
        print("[ADD BORROWER GROUP TRANSACTION] Successfully added borrower group transaction")
    except db.Error as e:
        print(f"[ADD BORROWER GROUP TRANSACTION] Error adding borrower group transaction: {e}")

# FUNCTION TO CREATE GROUP LOAN TRANSACTION
def createGroupTransaction(cursor: db.Cursor) -> None:
    # GROUP LOAN
    group_id = chooseGroup(cursor)
    if(group_id!=None): # will not run if there are no groups created yet
        transaction_amount = askAmount()
        transaction_date = getDate()
        isPaid = 0
        isGroupLoan = 1
        amountRemaining = transaction_amount # amount remaining to be paid set to transaction_amount
        userIsLender = get_user_is_lender()                 
        if userIsLender==1: # user is a lender
            lender = 1
            
            memCount = getMemberCount(cursor, group_id)
            initialAmount = transaction_amount/(memCount-1)
            dividedAmount = round(initialAmount, 2)
            members = getGroupMembers(cursor, group_id, lender)
            updateMembersBalance(cursor, members, dividedAmount)
            updateGroupBalance(cursor, group_id, transaction_amount)
            
            addLenderGroupTransaction(cursor, transaction_amount, transaction_date, isPaid, isGroupLoan, amountRemaining, dividedAmount, lender, group_id)
            transaction_id = cursor.lastrowid
            addIsCreatedBy(cursor, transaction_id, 1, group_id)
        else: # user is a borrower
            lender = chooseLender(cursor, group_id) # ask user to choose lender by showing username of members of the group
            
            memCount = getMemberCount(cursor, group_id)
            initialAmount = transaction_amount/(memCount-1)
            dividedAmount = round(initialAmount, 2)
            members = getGroupMembers(cursor, group_id, lender)
            updateMembersBalance(cursor, members, dividedAmount)
            updateGroupBalance(cursor, group_id, transaction_amount)
            
            addBorrowerGroupTransaction(cursor, transaction_amount, transaction_date, isPaid, isGroupLoan, amountRemaining, dividedAmount, lender, group_id)
            transaction_id = cursor.lastrowid
            addIsCreatedBy(cursor, transaction_id, 1, group_id)                
            
    # -----------------------------------------------------------------------    
    # [PROCESS for adding group transaction where user is the lender]
    # find borrowers by getting members of the group excluding user
    # update the outstanding balance of the borrowers (members of the group)
    # set group balance of group to group_balance += transaction_amount
    # add transaction to the table
            

# The add_expense function creates a single or group transaction
def add_expense(cursor: db.Cursor, connection: db.Connection) -> None: 
    try:
        transaction_creator = None
        while transaction_creator not in ['1','2']: # 1 = user, 2 = group
            transaction_creator = input("\nChoose Transaction Creator:\n[1] Single User Transaction\n[2] Group Transaction\nChoice: ")
            if transaction_creator=='1': # user transaction
                # input transaction amount
                transaction_amount = askAmount()
                transaction_date = getDate()
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
                    updateUserBalance(cursor, user_id, transaction_amount) # update user balance of borrower
                    
                else: # user is a borrower
                    user_id = 1 # user (with user_id 1) is the borrower
                    # ask user to select a lender
                    print("Choose a lender:")
                    getUsers(cursor)  # get the user count using the getUsers() function
                    lender = chooseFriend(getUserCount(cursor))  # get the chosen friend using the chooseFriend() function
                    userLendTransaction(cursor, transaction_amount, transaction_date, transaction_type, isLoan, lender, isPaid, user_id)
                    updateUserBalance(cursor, user_id, transaction_amount) # update user balance of borrower

            else: # group transaction (transaction_creator == 2)
                createGroupTransaction(cursor)
   
        connection.commit()
        print("[END] Successfully added transaction to the database")
    except db.Error as e:
        print(f"Error adding transaction to the database: {e}")
    return None

def delete_expense(cursor: db.Cursor) -> None:
    return None


def search_expense(cursor: db.Cursor) -> None:
    return None


def update_expense(cursor: db.Cursor) -> None:
    return None


def print_loans(loans: list) -> None:
    print("=====================================")
    print("\t\tLoans")
    print(tabulate(loans, tablefmt="rounded_grid"))
    print("=====================================")
    return None
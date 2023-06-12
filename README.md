# Money Tracking App
## Group 4
## CMSC 127 ST6L
* Araez, Danielle Lei R.  
* Concepcion, Sean Kierby I.  
* Despi, John Robertson C.  
  
# Project Description
This Python application, entitled, SplitTogether, is a terminal-based money tracking application that allows a user to track their lent and borrowed expenses with a friend or a group. The application allows the user to add, delete, search, and update an expense, friend, and group. The user can also generate summarized reports that display a detailed information about their expenses, friends, and groups in a tabular format.
  
# Project Features
## Add, Delete, Search, and Update an Expense  
The main features of the application include the add, delete, search, and update an expense, friend, or group.      
    
For the *add expense* functionality, the app allows the user to create a loan transaction with a friend (single-user) or group. The user can be the lender or the borrower. If the user is the lender, then, a borrower must be chosen for friend transactions. For group transactions, the borrower would automatically be the other members of the group. On the other hand, if the user is the borrower, then, a lender must be chosen for both the friend and group transactions.   
  
Meanwhile, the *delete expense* functionality enables the user to delete a paid loan transaction with a friend or group. This means that the user can only delete a transaction if it is already paid. Doing so would automatically delete the other transactions associated with the expense, that is, the settlement transactions for that loan.  
  
On the other hand, the *search expense* feature asks the user for the transaction ID of the expense. It shows the transaction amount, transaction date, transaction type (loan or settlement), and lender ID. If it is a friend transaction, it would show both the Lender and Borrower (User ID) IDs. If it is a group transaction, it would also display the Lender and Group ID, Amount Remaining to be paid to the lender, and Divided Amount, which is the equally divided amount to be paid by the members of the group to the lender, which is also a member inside the group. If the transaction is a settlement transaction, it would also show the settled loan (transaction ID).   
  
The *update expense* feature allows the user to settle a loan transaction if the user is a borrower in a friend or group transaction. It automatically settles the total amount to be paid by the user to the lender. For a group transaction, it updates the amount remaining to be paid for that group loan. Whereas, it updates the status of the friend transaction to already paid as it was already settled. 

An additional *edit expense* feature allows the user to edit the transaction amount of an unpaid loan transaction which automatically updates the outstanding balance of the user or members of the group. 
  
## Add, Delete, Search, and Update a Friend  
The application also allows the user to add, delete, search, and update a friend. In adding a friend, it asks the user to input the username and beginning outstanding balance of the friend. For deleting a friend, it shows the list of friends of the user and then asks the user to input the friend ID to be deleted. For searching a friend, the application would ask the user to enter the username of the friend and shows the outstanding balance of the friend if it exists. Lastly, for updating a friend, the application would ask the user to input the friend ID to be updated and then asks the user to input the new username of the friend.      
  
## Add, Delete, Search, and Update a Group  
For adding a group, the user is asked to input the group name. Afterwards, the list of friends along with their IDs would be shown wherein the user must input the user ID to add the friend to the group. For deleting a group, the list of groups would also be shown and inputting the Group ID would automatically delete the group along with the transactions involving that group. To search for a group, the user shall input the Group ID and it would show the Group ID, Group Name, Groub Balance, and Number of Members in a tabular format. For updating the group, the list of groups will be shown and upon inputting the Group ID, the user is asked to input a new group name which would update the name of the group.   

## Generate Reports
For generating reports, the user is asked to input the type of report to be generated. The user can choose from the following:
1. View All Expenses Made within a Month  
2. View All Expenses Made with a Friend  
3. View All Expenses Made with a Group  
4. View Current Balance from All Expenses  
5. View All Friends with Outstanding Balance  
6. View All Groups  
7. View All Groups with an Outstanding Balance  
  
## How to Use the Application  
* First, the user shall clone this repository using a code editor such as Visual Studio Code.    
  
* Before running the application, the user must have the required softwares (i.e., MariaDB, Python, packages) installed in their computer. You may see the *Steps for Creating a Python Virtual Environment* section below for the installation of the required packages by creating a Python virtual environment.   
  
* From the terminal, the user shall create the loan_tracker database in MariaDB by typing `sudo mariadb -u root -p` and then entering the password. Afterwards, the user shall input `source loan_tracker.sql` to create the database. Note that the user must be in the root directory of the project to be able to create the database.    
  
* After creating the database, the user shall type `python main.py` to run the application.    
  
* 
  
* To quit the application, the user must be at the main menu of the app so that the `[0] Exit` option would be shown. Typing `0` as the choice would end the program.      
  
## Screenshots  
  


## Steps for Creating a Python Virtual Environment  
  
# Installation  
1. Clone the repository
2. Create a new virtual environment using python3. (See [How to Create a Python Virtual Environment](#how-to-create-a-python-virtual-environment-windows))
3. Activate the virtual environment.
4. Install the requirements using `pip install -r requirements.txt`


# How to Create a Python Virtual Environment (Windows)
1. Open the command prompt at the root of the project.
2. Create a new virtual environment using `python -m venv env`
3. Activate the virtual environment using `env\Scripts\activate.bat`


# Setting Environment Variables
1. Create a new file named `.env` at the root of the project.
2. Add the following lines to the file:
```
PASSWORD={your database password}
```
3. Replace `{your database password}` with your database password.
4. Save the file.
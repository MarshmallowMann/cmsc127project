-- Group 2 ST6L
-- Araez, Danielle Lei R.
-- Concepcion, Sean Kierby I.
-- Despi, John Robertson C.

DROP DATABASE IF EXISTS loan_tracker;

CREATE DATABASE loan_tracker;
USE loan_tracker;

-- Create a USER table containing the ff:
-- user_id (primary key and auto-increment), username, balance
CREATE TABLE user(
    user_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    balance DECIMAL(8,2) DEFAULT 0 NOT NULL,
    PRIMARY KEY(user_id)
);

-- Create a GROUP table containing the ff: 
-- group_id (primary key and auto-increment), group_name, group_balance, num_of_members
CREATE TABLE `group`(
    group_id INT NOT NULL AUTO_INCREMENT,
    group_name VARCHAR(20) NOT NULL,
    group_balance DECIMAL(8,2) DEFAULT 0,
    num_of_members INT DEFAULT 0,
    PRIMARY KEY(group_id)
);

-- Create TRANSACTION table
-- Containing transaction_id (primary key and auto-increment), Amount, Date, Transaction Type,
-- isLoan, Lender, isPaid, isGroupLoan, amountRemaining, DividedAmount, isSettlement, SettledLoan(references another transactio_id)
-- User_id (references user_id from USER table), Group_id (references group_id from GROUP table)
CREATE TABLE transaction(
    transaction_id INT NOT NULL AUTO_INCREMENT,
    transaction_amount DECIMAL(8,2) NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(10) NOT NULL,
    isLoan BOOLEAN DEFAULT 0 NOT NULL,
    lender INT DEFAULT NULL, -- references user_id from USER table
    isPaid BOOLEAN DEFAULT 0,
    isGroupLoan BOOLEAN DEFAULT 0,
    amountRemaining DECIMAL(8,2) DEFAULT 0,
    dividedAmount DECIMAL(8,2) DEFAULT 0,
    isSettlement BOOLEAN DEFAULT 0 NOT NULL,
    settledLoan INT DEFAULT NULL,
    user_id INT NOT NULL,
    group_id INT DEFAULT NULL,
    PRIMARY KEY(transaction_id),
    CONSTRAINT transaction_userid_fk FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    CONSTRAINT transaction_settledLoan_fk FOREIGN KEY(settledLoan) REFERENCES transaction(transaction_id) ON DELETE CASCADE,
    CONSTRAINT transaction_groupid_fk FOREIGN KEY(group_id) REFERENCES `group`(group_id) ON DELETE CASCADE,
    CONSTRAINT transaction_lender_fk FOREIGN KEY(lender) REFERENCES user(user_id) ON DELETE CASCADE
);

-- Create a table IS_PART_OF containing the ff:
-- user_id (references user_id from USER table), group_id (references group_id from GROUP table)
CREATE TABLE is_part_of(
    user_id INT NOT NULL,
    group_id INT NOT NULL,
    PRIMARY KEY(user_id, group_id),
    CONSTRAINT ispartof_userid_fk FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    CONSTRAINT ispartof_groupid_fk FOREIGN KEY(group_id) REFERENCES `group`(group_id) ON DELETE CASCADE
);

-- Create a table IS_CREATED_BY containing the ff:
-- transaction_id (references transaction_id from TRANSACTION table),user_id (references user_id from USER table), group_id (references group_id from GROUP table)
CREATE TABLE is_created_by(
    transaction_id INT NOT NULL,
    user_id INT NOT NULL,
    group_id INT NOT NULL,
    PRIMARY KEY(transaction_id, user_id, group_id),
    CONSTRAINT iscreatedby_transactionid_fk FOREIGN KEY(transaction_id) REFERENCES transaction(transaction_id) ON DELETE CASCADE,
    CONSTRAINT iscreatedby_userid_fk FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    CONSTRAINT iscreatedby_groupid_fk FOREIGN KEY(group_id) REFERENCES `group`(group_id) ON DELETE CASCADE
);

CREATE TABLE is_made_by(
    transaction_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY(transaction_id, user_id),
    CONSTRAINT ismadeby_transactionid_fk FOREIGN KEY(transaction_id) REFERENCES transaction(transaction_id) ON DELETE CASCADE,
    CONSTRAINT ismadeby_userid_fk FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE,
);

-- Create a sample Add, delete, search, and update a user;
INSERT INTO user(username, balance) VALUES('Ilay', 0);



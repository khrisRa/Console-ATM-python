import sqlite3
import sys
import time
import os
import re

def tbcreator():
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE balances
        		("USER_ID"	INTEGER NOT NULL,
    	"acc"	INTEGER NOT NULL UNIQUE,
    	"balances"	FLOAT NOT NULL,
    	PRIMARY KEY("USER_ID" AUTOINCREMENT))''')
    c.execute("INSERT INTO balances(acc, balances) VALUES ('0', '0')")
    conn.commit()
    conn.close()


def db_check():
    conn = sqlite3.connect("accounts.db", timeout=1)
    c = conn.cursor()
    try:
        c.execute("UPDATE balances SET balances = '0' WHERE balances =?", ['0'])
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(e)
        print("Database might be locked check and run again")
        sys.exit()


def ac_create(acc, bal):
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM balances WHERE acc=?", [acc])
    if c.fetchone():
        print("cannot use this acc number, try with a different one \nplease wait...")
        time.sleep(2)
    else:
        c.execute("INSERT INTO balances(acc, balances) VALUES (?, ?)", [acc, bal])
        conn.commit()
        conn.close()
        print("Account created successfully \nplease wait...")
        time.sleep(2)


def deposit(acc, bal):
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM balances WHERE acc=?", [acc])
    if c.fetchone() is None:
        print("Account does not exist, try creating one \nplease wait...")
        time.sleep(2)
    else:
        c.execute("UPDATE balances SET balances = balances + ? WHERE acc =?", [bal, acc])
        conn.commit()
        conn.close()
        print("Deposit successfull \nplease wait...")
        time.sleep(2)


def withdraw(acc, bal):
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM balances WHERE acc=?", [acc])
    if c.fetchone() is None:
        print("Account does not exist, try creating one")
        time.sleep(2)
    else:
        c.execute("SELECT * FROM balances WHERE acc=? AND balances < ?", [acc, bal])
        if c.fetchone():
            print("Invalid amount check your balance")
            time.sleep(2)
        else:
            c.execute("UPDATE balances SET balances = balances - ? WHERE acc =?", [bal, acc])
            conn.commit()
            conn.close()
            print("Withdrawal successfull \nplease wait...")
            time.sleep(2)


def transfr(acc, acc2, bal):
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM balances WHERE acc=? OR acc=?", [acc, acc2])
    if c.fetchone() is None:
        print("Account(s) does not exist, try creating one")
        time.sleep(2)
    else:
        c.execute("SELECT * FROM balances WHERE acc=? AND balances < ?", [acc, bal])
        if c.fetchone():
            print("Invalid amount check your balance")
            time.sleep(2)
        else:
            c.execute("UPDATE balances SET balances = balances - ? WHERE acc =?", [bal, acc])
            c.execute("UPDATE balances SET balances = balances + ? WHERE acc =?", [bal, acc2])
            conn.commit()
            conn.close()
            print("Transfer successfull \nplease wait...")
            time.sleep(2)

    
def view():
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()    
    c.execute("SELECT acc, balances FROM balances WHERE balances != 0")
    record = c.fetchall()
    for row in record:
        print(
        'Account number:- ', row[0], "\n",
        'Balance:- ', row[1], "\n"
        )
        conn.close()
    else:
        print("no more accounts to display")
    conn.close()


def view_proc():
    while True:
        coni = (input("Do you wish to proceed ? (Y OR N): "))
        con = coni.lower()
        if con == "y":
            break            
        elif con == "n":
            try:
                os.remove("accounts.db")
                print("Good Bye closing and deleting in 5secs \nplease wait...")
                time.sleep(5)
                exit()
            except FileNotFoundError:
                print("file not existent closing in 5secs \nplease wait...")
                time.sleep(5)
                break
            except PermissionError:
                print("file in use on your system process")
        else:
            print("You have to press Y or N")


def check_in(twd):
    pattern = "^[0-9]*$"
    while not re.match(pattern, twd):
        twd = input("Enter account number (numbers): ")
    else:
        pass
    return twd


def check_amt(twd):
    pattern = "^[0-9.]*$"
    while not re.match(pattern, twd):
        twd = input("Enter amount up to two decimal places (numbers): ")
    else:
        pass
    return twd
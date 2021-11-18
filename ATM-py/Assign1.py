import os
import sqlite3
import mylib
import time

if os.path.exists("accounts.db"):
    mylib.db_check()
else:
    mylib.tbcreator()

while True:
    print("""
    Welcome to console banking application
        1. Create account
        2. Deposit
        3. Withdraw
        4. View accounts        
        5. Transfer between your accounts
        6. Exit
    """)
    Your_Choice = input("Please enter your choice :")

    if Your_Choice == "1":
        acc = mylib.check_in(input("Enter an account number (numbers only): "))
        bal = mylib.check_amt(input("Enter initial amount: "))
        mylib.ac_create(acc, bal)

    elif Your_Choice == "2":
        acc = mylib.check_in(input("Enter an account number (numbers only): "))
        bal = mylib.check_amt(input("Enter deposit amount: "))
        mylib.deposit(acc, bal)

    elif Your_Choice == "3":
        acc = mylib.check_in(input("Enter an account number (numbers only): "))
        bal = mylib.check_amt(input("Enter withdrawal amount: "))
        mylib.withdraw(acc, bal)

    elif Your_Choice == "4":
        try:
            mylib.view()
        except sqlite3.OperationalError:
            print("No accounts created yet") 
        mylib.view_proc()                       
    
    elif Your_Choice == "5":
        acc = mylib.check_in(input("Enter an account number to transfer from: "))
        acc2 = mylib.check_in(input("Enter an account number to transfer to: "))
        bal = mylib.check_amt(input("Enter transfer amount: "))
        mylib.transfr(acc, acc2, bal)

    elif Your_Choice == "6":
        try:
            os.remove("accounts.db")
            print("Good Bye closing and deleting in 5secs")
            time.sleep(5)
            break
        except FileNotFoundError:
            print("file not existent closing in 5secs")
            time.sleep(5)
            break
        except PermissionError:
                print("file in use on your system process")
                break
    else:
        print("You have to press 1 or 2 or 3 or 4 or 5 or 6")
    
    
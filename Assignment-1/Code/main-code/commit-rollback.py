import App 
from tabulate import tabulate
from decimal import Decimal
import numpy as np
import pandas 
# import 'your-code.py' as app;

# from code import yourCode

# Skeleton for commit and roll-back exercise    

# *** Your Code goes Here ***

# Your main program
def main():
    print("First Output:\n")
    print("Print Original Contents of Databases\n")
    print("\nOriginal Contents of Customers\n")
    cusD = App.customer_data 
    print(tabulate(cusD, headers=["Id","Last Name", "First Name", "Address", "City", "Age"],tablefmt="grid"))
    print("\tOriginal Contents of Account")
    accD= App.account_data
    print(tabulate(accD, headers=["Id", "Checking Account", "Saving Account"],tablefmt="grid"))
    print("\tOriginal Contents of Account_Balance")
    accDB= App.account_balance_data
    print(tabulate(accDB, headers=["Account Number", "Balance"],tablefmt="grid"))
    print("\n\nPrint current status of Log Sub-system\n")
    print("------------------Initial Status of the Log Sub-System---------------------------")
    printLog()
    print("---------------------------------------------------------------------------------")
    # print (tabulate(App.log, headers=["Transaction ID", "Table Name","Operation","Attribute Name","Transaction Time", "Account ID", "Before Transaction", "After Transaction" , "Transaction Complete", "Note"], tablefmt="grid"))



    # Transaction Block 1: Successful
    print("\n\nBLOCK TRANSACTION 1")
    print("Subtract money from one account.")
    print("Add money to second one")
    print("COMMIT all your changes")
    App.success_driver()
    # read value of sub transaction 1 note 
    # read value of sub transaction 2 value 
    printOutNote(0)
    print("Print Contents of Databases")
    print("\t Contents of Customers")
    cusD = App.customer_data 
    print(tabulate(cusD, headers=["Id","Last Name", "First Name", "Address", "City", "Age"],tablefmt="grid"))
    
    print("\t Contents of Account")
    accD= App.account_data
    print(tabulate(accD, headers=["Id", "Checking Account", "Saving Account"],tablefmt="grid"))
    
    print("\t Contents of Account_Balance")
    accDB2= App.account_balance_data
    print(tabulate(accDB2, headers=["Account Number", "Balance"],tablefmt="grid"))
    
    print("Print current status of Log Sub-system\n")
    print("------------------After BLOCK TRANSACTION 1---------------------------")
    printLog()
    print("---------------------------------------------\n\n\n")
    
    print("BLOCK TRANSACTION 2")
    print("Subtract money from one account (Same Transaction than before)")
    print("\t Initial Contents of Account_Balance")
    print(tabulate(App.account_balance_data, headers=["Account Number", "Balance"],tablefmt="grid"))
   
    App.fail_driver()
    print("\nFailure occurs!!!!!!! ACTION REQUIRED")
    print("Must either AUTOMATICALLY Roll-back Database to a state of equilibrium (Bonus), OR\nSTOP Operations and show: (a) Log-Status, and (b) Databases Contents.\n")
    print("\nThe Log Sub-system contents should show the necessary operations needed to fix the situation!")
    print("\t Contents of Account_Balance")
    accDB3= App.account_balance_data
    print(tabulate(accDB3, headers=["Account Number", "Balance"],tablefmt="grid"))

    print("Print current status of Log Sub-system\n")
    print("------------------After BLOCK TRANSACTION 2---------------------------")
    printLog()
    print("---------------------------------------------")
    App.saveToLog()
    printOutNote(1)


def printOutNote(num):
    if App.log:
        count1 =0

        # for arrayOb in App.log:
        print("Transaction_Id:\t",App.log[num]['Transaction_ID'])
        print("\tSub_transaction1 - Status:\t",App.log[num]['sub_transaction1']['note'])
        print("\tSub_Transaction2 - Status:\t",App.log[num]['sub_transaction2']['note'])
        print("\tCommit Status:\t",App.log[num]['commit_status'])

## this function is called to print out the current status of the Log
def printLog():
    if App.log:
        count1 =0
        for arrayOb in range(0,len(App.log)):
            print("Log",count1+1)
            # print("New Log:\n")
            counter1 =0
            for key in App.log[arrayOb]:
                # print(key,":\t",App.log[arrayOb][key])
                print(key,":\t")
                if key=='Transaction_ID' :
                    print(App.log[arrayOb]['Transaction_ID'])
                elif key=='sub_transaction1':
                    for ob in App.log[arrayOb]['sub_transaction1']:
                        print("\t",ob,":\t",App.log[arrayOb]['sub_transaction1'][ob])
                elif key == 'sub_transaction2':
                    for ob in App.log[arrayOb]['sub_transaction2']:
                        print("\t",ob,":\t",App.log[arrayOb]['sub_transaction2'][ob])
                elif key=='before_image':
                    print("\t",App.log[arrayOb]['before_image'])
                elif key=='commit_status':
                    print("\t",App.log[arrayOb]['commit_status'])
                counter1 += 1
            count1+=1
    else:
        print("Log is empty!")
main()


import App 
from tabulate import tabulate
from decimal import Decimal

import pandas 
# import 'your-code.py' as app;

# from code import yourCode

# Skeleton for commit and roll-back exercise    

# *** Your Code goes Here ***

# Your main program
def main():
    print("First Output:")
    print("\nPrint Original Contents of Databases")

    print("\tOriginal Contents of Customers")
    cusD = App.customer_data 
    print(tabulate(cusD, headers=["Id","Last Name", "First Name", "Address", "City", "Age"],tablefmt="grid"))
    
    print("\tOriginal Contents of Account")
    accD= App.account_data
    print(tabulate(accD, headers=["Id", "Checking Account", "Saving Account"],tablefmt="grid"))
    
    print("\tOriginal Contents of Account_Balance")
    
    accD= App.account_balance_data
    print(accD)
    print(tabulate(accD, headers=["Account Number", "Balance"],tablefmt="grid"))
    

    print("\n\nPrint current status of Log Sub-system\n")
    print(App.log)
    print ( tabulate(App.log, headers=["Transaction ID", "Table Name","Operation","Attribute Name","Transaction Time", "Account ID", "Before Transaction", "After Transaction" , "Transaction Complete", "Note"]))
   

    # Transaction Block 1: Successful
    print("\n\nBLOCK TRANSACTION 1")
    print("Subtract money from one account.")
    print("Add money to second one")
    print("COMMIT all your changes")
    App.success_driver()
    App.success_driver()
    print("Print Contents of Databases")
    print("\t Contents of Customers")
    cusD = App.customer_data 
    print(tabulate(cusD, headers=["Id","Last Name", "First Name", "Address", "City", "Age"],tablefmt="grid"))
    
    print("\t Contents of Account")
    accD= App.account_data
    print(tabulate(accD, headers=["Id", "Checking Account", "Saving Account"],tablefmt="grid"))
    
    print("\t Contents of Account_Balance")
    accD= App.account_balance_data
    print(tabulate(accD, headers=["Account Number", "Balance"],tablefmt="grid"))
    
    print("Print current status of Log Sub-system\n")
    # before = App.log[0]["before_image"]

    for row in App.log:
        print(row.value)
        row["before_image"] = type(row["before_image"])
        
    # App.log["Log 1"]["before_image"] = type(App.log["Log 1"]["before_image"])
    # print("before", before)
    # App.log[0]["after_image"] = ["after Image"]
    
    # print(tabulate(App.log[0], headers=["Trans Id", "TBL Name", "operation", "Attr Name", "Trans Time", "Acct ID","before_Image","after_image", "Status","note"],tablefmt="grid"))
    print("\n\n\n\n")
    

    print(App.log)
    df = pandas.DataFrame(App.log)
    print(tabulate(df.T, headers="keys"))

    # print(df)
    # Transaction Block 1: Fails!
    print("BLOCK TRANSACTION 2")
    print("Subtract money from one account (Same Transaction than before)")
    print("Failure occurs!!!!!!! ACTION REQUIRED")
    print("Must either AUTOMATICALLY Roll-back Database to a state of equilibrium (Bonus), OR\nSTOP Operations and show: (a) Log-Status, and (b) Databases Contents.\n")
    print("\nThe Log Sub-system contents should show the necessary operations needed to fix the situation!")
    
main()
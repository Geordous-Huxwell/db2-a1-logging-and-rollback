# Your Code
import csv
import uuid
from datetime import datetime

log = []
customer_data = []
account_data = []
account_balance_data = []

def file_reader(tablename, filepath): #def is a function definition. so function file_reader(parameter, parameter)
    global customer_data, account_data, account_balance_data  #setting global variables 
    with open(filepath, 'r') as file:# open file with (filepath, 'r' r means open file for reading)
        if tablename == 'customer':  # if csv name (tablename) is customer then
            customer_data = list(csv.reader(file)) # then put it in the customer_data array, list() creates a list object, csv.reader() is used to read the file, which returns an iterable reader object
        elif tablename == 'account':  # else if csv name (called tablename) is account
            account_data = list(csv.reader(file))   #then put the information into the account_data array
        elif tablename == 'account_balance': # else if table name is account_balance
            account_balance_data = list(csv.reader(file)) # put it in the account_balance_data array
            account_balance_data = [[row[0], int(row[1])] for row in account_balance_data] # this line changes the account balances into integers. 
            # print(account_balance_data)

# this function gets the customer by there id, it does this 
# by looping through the customer data, and if each customer first column [0]
# then it returns the customer object.      
def getCustomerById(id):
    for customer in customer_data: # for each customer in customer_data 
        if customer[0] == id: # if customer column 1 value == id (param)
            return customer  # return the customer object
# this function gets the accounts by customer id, 
#  by looping through all the account_data arrays each account
# and if the account first column value is equal to the id (param),
#  then return the account. 
def getAccountsByCustId(id):
    for account in account_data:
        if account[0] == id:
            return account
# this function gets the account balance by id, it passes in the account id your
# looking for and loops through all the balances in the account balance data array 
# and checks there balance[0] first column which is the account id is equal to the param 
# then it returns the balance amount of the account you found. 
def getAccountBalanceById(acct_id):
    for balance in account_balance_data:
        if balance[0] == acct_id:
            return balance[1]
# this function is passed in the account and the amount wanted to be withdrawed 
# then in the function they loop through all the account_balance to find the row with 
# the same account number as the parameter acct_id passed in. once found it takes the
# second attribute account[1] which is the balance of that account and takes 
# away the amount passed in as a parameter from it.  
def withdraw(acct_id, amount):
    for account in account_balance_data:
        if account[0] == acct_id:
            account[1] = account[1] - amount
# this function is passed in the account id and the amount wanted to put into that account.
# it loops through all the account_balance data to find the row with the same account number. 
# Then when they find that row with the same accountNum and acct_id passed in it adds the 
# amount passed in as a parameter to the accountNum's balance. if after going through the whole 
# loop the acct_id never is found it would print a invalid statement and call the logger function
# to log the invalid deposit. 
def deposit(acct_id, amount):
    for account in account_balance_data:
        if account[0] == acct_id:
            account[1] = account[1] + amount
            return
    print('invalid account id')
    # logger(from_acct_id, before_image, False, "invalid deposit account id")
    raise Exception('invalid deposit account id')


def executeTransfer(from_acct_id, to_acct_id, amount):
    global account_balance_data
    before_image = account_balance_data
    from_acct_balance = getAccountBalanceById(from_acct_id)

    if from_acct_balance > amount: #if the balance of money in your account your taking from is greater then the amount then
        try:
            withdraw(from_acct_id, amount) # send to the withdraw function.
        except:
            logger(from_acct_id, before_image, False, "invalid withdraw account id")
            return False
        
        
        try:
            deposit(to_acct_id, amount) 
        except Exception as msg:
            print('deposit failed')
            print(msg.getMembers())
            logger(from_acct_id, before_image, False, msg)
            return False
        
        # print('after trans: ', account_balance_data)
        logger(from_acct_id, before_image, True, "success")
        return True
    else:
        logger(from_acct_id, before_image, False, "insufficient funds")
        return False
# this function logs all the different subtransactions. so all actions being taken will be 
# recorded in the log via this function being called. 
def logger(acct_id, before_image, trans_completed, note):
    global log
    transaction_id = uuid.uuid1() # uuid is a python library that generates a random id 
    transaction_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S") # this just gets the time of the transaction
    
    log.append({'transID':transaction_id, 
                'table_name':'account_balance',
                'operation':'update',
                'attribute_name':'balance',
                'trans_time':transaction_time, 
                'accountID':acct_id, 
                'before_image':before_image,
                'after_image':account_balance_data,
                'trans_completed':trans_completed,
                'note':note})

# these are all just reading different files in to get there data
#file_reader('customer','Assignment-1/Data-Assignment-1/csv/customer.csv')
file_reader('customer','Data-Assignment-1/csv/customer.csv') 

file_reader('account_balance','Data-Assignment-1/csv/account-balance.csv')
file_reader('account','Data-Assignment-1/csv/account.csv')

# print(customer_data)
# print(getCustomerById('3'))
# print(getAccountsByCustId('3'))


def success_driver():
    customer = getCustomerById('3') 
    customer_accts = getAccountsByCustId('3')
    chequing_acct = customer_accts[1]
    savings_acct = customer_accts[2]
    chequing_bal = getAccountBalanceById(chequing_acct)
    savings_bal = getAccountBalanceById(savings_acct)

    print(getAccountBalanceById(chequing_acct))

    executeTransfer(chequing_acct, savings_acct, 100000)
    print(log)

def fail_driver():
    customer_accts = getAccountsByCustId('3')
    chequing_acct = customer_accts[1]
    savings_acct = 000000 #invalid account id
    
    executeTransfer(chequing_acct, savings_acct, 100000)
    print(log)

#fail_driver()

success_driver()

# print original contents of DB 

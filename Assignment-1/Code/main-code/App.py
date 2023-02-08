# Your Code
import copy
import csv
import uuid
from datetime import datetime
from tabulate import tabulate

log = []
customer_data = []
account_data = []
account_balance_data = []
sub_trans_counter = 1
transaction_counter = 0 #read log file to get initial value by reading num rows

def file_reader(tablename, filepath):
    global customer_data, account_data, account_balance_data
    with open(filepath, 'r') as file:
        if tablename == 'customer':
            customer_data = list(csv.reader(file))
        elif tablename == 'account':
            account_data = list(csv.reader(file))
        elif tablename == 'account_balance':
            account_balance_data = list(csv.reader(file))
            account_balance_data = [[row[0], int(row[1])] for row in account_balance_data]
            # print(account_balance_data)
        
def getCustomerById(id):
    for customer in customer_data:
        if customer[0] == id:
            return customer

def getAccountsByCustId(id):
    for account in account_data:
        if account[0] == id:
            return account

def getAccountBalanceById(acct_id):
    for balance in account_balance_data:
        if balance[0] == acct_id:
            return balance[1]

def withdraw(acct_id, amount):
    for balance in account_balance_data:
        print(balance[0], acct_id)
        if balance[0] == acct_id:
            balance[1] = balance[1] - amount
            return
    raise Exception('invalid withdrawal account id')

def deposit(acct_id, amount):
    for balance in account_balance_data:
        if balance[0] == acct_id:
            balance[1] = balance[1] + amount
            return
    print('invalid account id')
    raise Exception('invalid deposit account id')


def executeTransfer(from_acct_id, to_acct_id, amount):
    global account_balance_data
    transaction_id = uuid.uuid1().int
    log.append({
                'Transaction_ID': transaction_id,
                'sub_transaction1':{},
                'sub_transaction2':{}
                })
    before_image = copy.deepcopy(account_balance_data)
    print('intitial account balance', before_image[2])
    from_acct_balance = getAccountBalanceById(from_acct_id)

    if from_acct_balance > amount:
        try:
            withdraw(from_acct_id, amount)
            logger(from_acct_id, before_image, True, "success")
            print('post-withdraw account balance', account_balance_data[2])

        except Exception as msg:
            print('withdraw failed')
            logger(from_acct_id, before_image, False, msg)
            return False

        try:
            deposit(to_acct_id, amount)
            logger(from_acct_id, before_image, True, "success")

        except Exception as msg:
            print('deposit failed')
            logger(from_acct_id, before_image, False, msg)
            return False
        
        return True
    else:
        logger(from_acct_id, before_image, False, "insufficient funds")
        return False

def logger(acct_id, before_image, trans_completed, note):
    global log, sub_trans_counter, transaction_counter

    transaction_id = uuid.uuid1().int
    transaction_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    sub_transaction = f"sub_transaction{sub_trans_counter}"
    # will need solve the index being hardcoded if we want our logger to be persistent (not be overwritten everytime the programs runs)
    # TODO: make subtransaction class
    log[transaction_counter][sub_transaction] = {
                'transID':transaction_id, 
                'table_name':'account_balance',
                'operation':'update',
                'attribute_name':'balance',
                'trans_time':transaction_time, 
                'accountID':acct_id, 
                # 'before_image':before_image,
                # 'after_image':account_balance_data,
                'trans_completed':trans_completed,
                'note': str(note)
                }
    if sub_trans_counter == 1:
        log[transaction_counter]['before_image'] = copy.deepcopy(before_image)
    
    sub_trans_counter += 1
 

def commitCheck(transaction_id):
    global log, transaction_counter, sub_trans_counter
    for transaction in log:
        if transaction['Transaction_ID'] == transaction_id:

            if transaction['sub_transaction1'].get('trans_completed') == True and transaction['sub_transaction2'].get('trans_completed') == True:
                commit()
            else:
                rollback(transaction_id)            
    
    transaction_counter += 1
    sub_trans_counter = 1
    

def commit():
    print("commit")
    with open('testy.csv', 'w', newline='') as csvfile:
        twriter = csv.writer(csvfile, delimiter=',',
                            quotechar=',', quoting=csv.QUOTE_MINIMAL)
        for row in account_balance_data:
            twriter.writerow(row)

def rollback(transaction_id):
    global log, account_balance_data
    # print("rollback")
    # print('failing subtrans id: ', subtrans_id)
    for transaction in log:
        # print('transaction', transaction)
        if transaction['Transaction_ID'] == transaction_id:
            print('before image',transaction['before_image'])
            account_balance_data = copy.deepcopy(transaction['before_image'])
            print('rollback account balance', account_balance_data[2])

            

file_reader('customer','Assignment-1/Data-Assignment-1/csv/customer.csv')
file_reader('account_balance','Assignment-1/Data-Assignment-1/csv/account-balance.csv')
file_reader('account','Assignment-1/Data-Assignment-1/csv/account.csv')



def success_driver():
    customer = getCustomerById('3')
    customer_accts = getAccountsByCustId('3')
    chequing_acct = customer_accts[1]
    savings_acct = customer_accts[2]

    chequing_bal = getAccountBalanceById(chequing_acct)
    savings_bal = getAccountBalanceById(savings_acct)
    amount = 100000
    print(getAccountBalanceById(chequing_acct))

    executeTransfer(chequing_acct, savings_acct, amount)
    print(log)
    commitCheck(log[0]['Transaction_ID'])


def fail_driver():
    customer_accts = getAccountsByCustId('3')
    chequing_acct = customer_accts[1]
    savings_acct = 000000 #invalid account id
    amount = 100000
    executeTransfer(chequing_acct, savings_acct, amount)
    print(log)
    commitCheck(log[0]['Transaction_ID'])

# Note this is going into a new testy file atm we can change after!
 

# fail_driver()

success_driver()



# Your Code
# import csv
# import uuid
# from datetime import datetime
# from tabulate import tabulate

# log = {}
# customer_data = []
# account_data = []
# account_balance_data = []

# class Log2:
#     def __init__(self,id , ):
#         self.trans_id= '123FakeID'
#         self.sub_trans1 = self.SubTrans1()
#         self.sub_trans2 = self.subTrans2()
#         # self.commit= self.commitStatus()
#         self.commit='YAYAY'
#     def show(self):
#         print ('id:', self.trans_id)
#         print ('subTrans1:', self.trans_id)
#         print ('subTrans2:', self.trans_id)
#         print ('commitStatus:', self.trans_id)
# class SubTrans1:
#     def __init__(self):
#         self.id = 'subID45564'
#         self.type = 'withdraw'
#         self.details= 'details'
#         self.sucess = 'success'
#     def display(self):
#         print ('Id:', self.id)
#         print ('Type:', self.type)
#         print ('Details:', self.details)
#         print ('Complete:', self.sucess)
# class SubTrans2:
#     def __init__(self):
#         self.id = 'subID45564'
#         self.type = 'withdraw'
#         self.details= 'details'
#         self.sucess = 'success'
#     def display(self):
#         print ('Id:', self.id)
#         print ('Type:', self.type)
#         print ('Details:', self.details)
#         print ('Complete:', self.sucess)

#makes a object thing 
# testy= Log2()
# testy.show()


# def file_reader(tablename, filepath): #def is a function definition. so function file_reader(parameter, parameter)
#     global customer_data, account_data, account_balance_data  #setting global variables 
#     with open(filepath, 'r') as file:# open file with (filepath, 'r' r means open file for reading)
#         if tablename == 'customer':  # if csv name (tablename) is customer then
#             customer_data = list(csv.reader(file)) # then put it in the customer_data array, list() creates a list object, csv.reader() is used to read the file, which returns an iterable reader object
#         elif tablename == 'account':  # else if csv name (called tablename) is account
#             account_data = list(csv.reader(file))   #then put the information into the account_data array
#         elif tablename == 'account_balance': # else if table name is account_balance
#             account_balance_data = list(csv.reader(file)) # put it in the account_balance_data array
#             account_balance_data = [[row[0], int(row[1])] for row in account_balance_data] # this line changes the account balances into integers. 
#             # print(account_balance_data)

# this function gets the customer by there id, it does this 
# by looping through the customer data, and if each customer first column [0]
# then it returns the customer object.      
# def getCustomerById(id):
#     for customer in customer_data: # for each customer in customer_data 
#         if customer[0] == id: # if customer column 1 value == id (param)
#             return customer  # return the customer object
# this function gets the accounts by customer id, 
#  by looping through all the account_data arrays each account
# and if the account first column value is equal to the id (param),
#  then return the account. 
# def getAccountsByCustId(id):
#     for account in account_data:
#         if account[0] == id:
            # return account
# this function gets the account balance by id, it passes in the account id your
# looking for and loops through all the balances in the account balance data array 
# and checks there balance[0] first column which is the account id is equal to the param 
# then it returns the balance amount of the account you found. 
# def getAccountBalanceById(acct_id):
#     for balance in account_balance_data:
#         if balance[0] == acct_id:
            # return balance[1]
# this function is passed in the account and the amount wanted to be withdrawed 
# then in the function they loop through all the account_balance to find the row with 
# the same account number as the parameter acct_id passed in. once found it takes the
# second attribute account[1] which is the balance of that account and takes 
# away the amount passed in as a parameter from it.  
# def withdraw(acct_id, amount):
#     for account in account_balance_data:
#         if account[0] == acct_id:
#             account[1] = account[1] - amount
# this function is passed in the account id and the amount wanted to put into that account.
# it loops through all the account_balance data to find the row with the same account number. 
# Then when they find that row with the same accountNum and acct_id passed in it adds the 
# amount passed in as a parameter to the accountNum's balance. if after going through the whole 
# loop the acct_id never is found it would print a invalid statement and call the logger function
# to log the invalid deposit. 
# def deposit(acct_id, amount):
#     for account in account_balance_data:
#         if account[0] == acct_id:
#             account[1] = account[1] + amount
#             return
#     print('invalid account id')
#     raise Exception('invalid deposit account id')
    

# def executeTransfer(from_acct_id, to_acct_id, amount):
#     global account_balance_data
    
#     before_image = account_balance_data
#     from_acct_balance = getAccountBalanceById(from_acct_id)

#     if from_acct_balance > amount: #if the balance of money in your account your taking from is greater then the amount then
#         try: 
#             withdraw(from_acct_id, amount) # send to the withdraw function.
#         except Exception as msg: 
#             print('withdraw failed')
#             logger(from_acct_id, before_image, False, msg)
#             return False 
        
#         try: 
#             deposit(to_acct_id, amount) 
#         except Exception as msg: 
#             print('deposit failed')
#             logger(from_acct_id, before_image, False, msg)
#             return False

#         logger(from_acct_id, before_image, True, "success")
#         return True
#     else:
#         logger(from_acct_id, before_image, False, "insufficient funds")
#         return False

# this function logs all the different subtransactions. so all actions being taken will be 
# recorded in the log via this function being called. 
# def logger(acct_id, before_image, trans_completed, note):
#     global log
#     transaction_id = uuid.uuid1().int # uuid is a python library that generates a random id 
#     transaction_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S") # this just gets the time of the transaction
    
    # log.append({'transID':[transaction_id, tabulate(account_data)], 
    #             'table_name':['account_balance', 2],
    #             'operation':['update', 2],
    #             'attribute_name':['balance', 2],
    #             'trans_time':[transaction_time, 2], 
    #             'accountID':[acct_id, 2], 
    #             'before_image':[before_image, 2],
    #             'after_image':[account_balance_data, 2],
    #             'trans_completed':[trans_completed, 2],
    #             'note':[note, 2]})
    
    # log[transaction_id] = {
    #     # 'transID':transaction_id , 
    #                             'table_name':'account_balance',
    #                             'operation':'update',
    #                             'attribute_name':'balance',
    #                             'trans_time':transaction_time,
    #                             'accountID':acct_id, 
    #                             'before_image':before_image,
    #                             # 'after_image':account_balance_data,
    #                             'trans_completed':trans_completed, 
    #                             'note':note, }
# these are all just reading different files in to get there data
#file_reader('customer','Assignment-1/Data-Assignment-1/csv/customer.csv')
# file_reader('customer','Data-Assignment-1/csv/customer.csv') 

# file_reader('account_balance','Data-Assignment-1/csv/account-balance.csv')
# file_reader('account','Data-Assignment-1/csv/account.csv')

# print(customer_data)
# print(getCustomerById('3'))
# print(getAccountsByCustId('3'))


# def success_driver():
#     customer = getCustomerById('3') 
#     customer_accts = getAccountsByCustId('3')
#     chequing_acct = customer_accts[1]
#     savings_acct = customer_accts[2]
#     chequing_bal = getAccountBalanceById(chequing_acct)
#     savings_bal = getAccountBalanceById(savings_acct)

#     # print(getAccountBalanceById(chequing_acct))

#     executeTransfer(chequing_acct, savings_acct, 100000)
#     # print(log)

# def fail_driver():
#     customer_accts = getAccountsByCustId('3')
#     chequing_acct = customer_accts[1]
#     savings_acct = 000000 #invalid account id
    
#     executeTransfer(chequing_acct, savings_acct, 100000)
    # print(log)

#fail_driver()

# success_driver()

# print original contents of DB 
    

#     executeTransfer(chequing_acct, savings_acct, amount)
#     print(log)

# fail_driver()
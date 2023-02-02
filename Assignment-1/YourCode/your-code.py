# Your Code
import csv
import uuid
from datetime import datetime

log = []
customer_data = []
account_data = []
account_balance_data = []

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
        if balance[0] == acct_id:
            balance[1] = balance[1] - amount

def deposit(acct_id, amount):
    for balance in account_balance_data:
        if balance[0] == acct_id:
            balance[1] = balance[1] + amount
            return
    print('invalid account id')
    # logger(from_acct_id, before_image, False, "invalid deposit account id")
    raise Exception('invalid deposit account id')


def executeTransfer(from_acct_id, to_acct_id, amount):
    global account_balance_data
    before_image = account_balance_data
    from_acct_balance = getAccountBalanceById(from_acct_id)

    if from_acct_balance > amount:
        try:
            withdraw(from_acct_id, amount)
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

def logger(acct_id, before_image, trans_completed, note):
    global log
    transaction_id = uuid.uuid1()
    transaction_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
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


file_reader('customer','Assignment-1/Data-Assignment-1/csv/customer.csv')
file_reader('account_balance','Assignment-1/Data-Assignment-1/csv/account-balance.csv')
file_reader('account','Assignment-1/Data-Assignment-1/csv/account.csv')

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

fail_driver()
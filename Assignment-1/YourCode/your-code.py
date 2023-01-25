# Your Code
import csv

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

def executeTransaction(from_acct_id, to_acct_id, amount):
    from_acct_balance = getAccountBalanceById(from_acct_id)
    to_acct_balance = getAccountBalanceById(to_acct_id)

    if from_acct_balance > amount:
        from_acct_balance = from_acct_balance - amount
        to_acct_balance = to_acct_balance + amount
        return True
    else:
        return False

# def logger():


file_reader('customer','Assignment-1\Data-Assignment-1\csv\customer.csv')
file_reader('account_balance','Assignment-1\Data-Assignment-1\csv\/account-balance.csv')
file_reader('account','Assignment-1\Data-Assignment-1\csv\/account.csv')

# print(customer_data)
# print(getCustomerById('3'))
# print(getAccountsByCustId('3'))

customer = getCustomerById('3')
customer_accts = getAccountsByCustId('3')
chequing_acct = customer_accts[1]
savings_acct = customer_accts[2]
chequing_bal = getAccountBalanceById(chequing_acct)
savings_bal = getAccountBalanceById(savings_acct)

print(getAccountBalanceById(chequing_acct))


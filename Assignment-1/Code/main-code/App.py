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
transaction_counter = 0 

def file_reader(tablename, filepath):
    """reads in a csv file and stores the data in a global variable"""
    global customer_data, account_data, account_balance_data, db
    with open(filepath, 'r') as file:
        if tablename == 'customer':
            customer_data = list(csv.reader(file))
        elif tablename == 'account':
            account_data = list(csv.reader(file))
        elif tablename == 'account_balance':
            account_balance_data = list(csv.reader(file))
            account_balance_data = [[row[0], int(row[1])] for row in account_balance_data]

        
def getCustomerById(id):
    """returns a customer record by id"""
    for customer in customer_data:
        if customer[0] == id:
            return customer

def getAccountsByCustId(id):
    """returns a list of account records by customer id"""
    for account in account_data:
        if account[0] == id:
            return account

def getAccountBalanceById(acct_id):
    """returns the balance of an account by account id"""
    for balance in account_balance_data:
        if balance[0] == acct_id:
            return balance[1]

def withdraw(acct_id, amount):
    """withdraws an amount from an account by account id"""
    for balance in account_balance_data:
        if balance[0] == acct_id:
            balance[1] = balance[1] - amount
            return
    raise Exception('invalid withdrawal account id')

def deposit(acct_id, amount):
    """deposits an amount into an account by account id"""
    for balance in account_balance_data:
        if balance[0] == acct_id:
            balance[1] = balance[1] + amount
            return
    raise Exception('invalid deposit account id')


def executeTransfer(from_acct_id, to_acct_id, amount):
    """executes a transfer between two accounts"""
    global account_balance_data
    transaction_id = uuid.uuid1().int

    # set up log entry for the transaction
    log.append({
                'Transaction_ID': transaction_id,
                'sub_transaction1':{},
                'sub_transaction2':{}
                })
    
    # retain an image of the account balance data before the transaction
    before_image = copy.deepcopy(account_balance_data)
    from_acct_balance = getAccountBalanceById(from_acct_id)

    if from_acct_balance > amount:
        try:
            withdraw(from_acct_id, amount)
            logger(from_acct_id, before_image, True, "success")

        except Exception as msg:
            logger(from_acct_id, before_image, False, msg)
            return False

        try:
            deposit(to_acct_id, amount)
            logger(from_acct_id, before_image, True, "success")

        except Exception as msg:
            logger(from_acct_id, before_image, False, msg)
            return False
        
        return True
    else:
        logger(from_acct_id, before_image, False, "insufficient funds")
        return False

def logger(acct_id, before_image, trans_completed, note):
    """logs the details of a transaction"""
    global log, sub_trans_counter, transaction_counter

    transaction_id = uuid.uuid1().int
    transaction_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    sub_transaction = f"sub_transaction{sub_trans_counter}"
    log[transaction_counter][sub_transaction] = {
                'transID':transaction_id, 
                'table_name':'account_balance',
                'operation':'update',
                'attribute_name':'balance',
                'trans_time':transaction_time, 
                'accountID':acct_id, 
                'trans_completed':trans_completed,
                'note': str(note)
                }
    # preserve the before image of the account balance data only if it is the first sub transaction
    if sub_trans_counter == 1:
        log[transaction_counter]['before_image'] = copy.deepcopy(before_image)
    
    sub_trans_counter += 1
 
def commitCheck(transaction_id):
    """checks if a transaction is ready to be committed or needs to be rolled back to before image"""
    global log, transaction_counter, sub_trans_counter
    for transaction in log:
        if transaction['Transaction_ID'] == transaction_id:

            if transaction['sub_transaction1'].get('trans_completed') == True and transaction['sub_transaction2'].get('trans_completed') == True:
                commit()
                log[transaction_counter]['commit_status']= True
            else:
                print("\tafter withdraw success but before Rollback(Contents of Account_Balance): ")
                print(tabulate(account_balance_data, headers=["Account Number", "Balance"],tablefmt="grid"))
                rollback(transaction_id)   
                log[transaction_counter]['commit_status']= False      
    
    transaction_counter += 1
    # reset the sub transaction counter for the next block transaction
    sub_trans_counter = 1
    

def commit():
    """commits the transaction back to secondary memory (csv files)"""
    global db
    fileNames=db.keys()
    
    for fileName in fileNames:
        with open(f'Assignment-1/Data-Assignment-1/csv/{fileName}.csv', 'w', newline='') as csvfile:
            twriter = csv.writer(csvfile, delimiter=',',
                            quotechar=',', quoting=csv.QUOTE_MINIMAL)
            currList = db[fileName]
            for row in currList:
                twriter.writerow(row)
    print("commited!")

def rollback(transaction_id):
    """rolls back the transaction to the before image of the database"""
    global log, account_balance_data
    for transaction in log:
        if transaction['Transaction_ID'] == transaction_id:
            account_balance_data = copy.deepcopy(transaction['before_image'])

# read the csv files into main memory            
file_reader('customer','Assignment-1/Data-Assignment-1/csv/customer.csv')
file_reader('account_balance','Assignment-1/Data-Assignment-1/csv/account-balance.csv')
file_reader('account','Assignment-1/Data-Assignment-1/csv/account.csv')
# assign the red in data to the db dictionary
db = {'customer': customer_data, 'account': account_data, 'account-balance': account_balance_data}




def success_driver():
    """driver function to simulate a successful transaction"""
    global transaction_counter
    customer = getCustomerById('3')
    customer_accts = getAccountsByCustId('3')
    chequing_acct = customer_accts[1]
    savings_acct = customer_accts[2]

    # chequing_bal = getAccountBalanceById(chequing_acct)
    # savings_bal = getAccountBalanceById(savings_acct)
    amount = 100000

    executeTransfer(chequing_acct, savings_acct, amount)
    commitCheck(log[transaction_counter]['Transaction_ID'])


def fail_driver():
    """driver function to simulate a failed transaction"""
    global transaction_counter
    customer_accts = getAccountsByCustId('3')
    chequing_acct = customer_accts[1]
    savings_acct = 000000 #invalid account id
    amount = 100000

    executeTransfer(chequing_acct, savings_acct, amount)
    commitCheck(log[transaction_counter]['Transaction_ID'])


def saveToLog():
    """saves the transaction log to a file"""
    with open("file.txt", "w", encoding="utf-8") as f:
        f.write("\u0332".join("Logging sub-system status"))
        count = 1
        for arrayOb in range(0,len(log)):
            # f.write(f'\n\nLog {count}:\n')
            f.write('\n\nTransaction:\n')
            counter= 0
            for key in log[arrayOb]:

                f.write(f'{key}:\t\n')
                if key=='Transaction_ID' :
                    f.write(f'{log[arrayOb][key]}\n')
                elif key=='sub_transaction1':
                    for ob in log[arrayOb]['sub_transaction1']:
                        f.write(f'\t{ob}:\t{log[arrayOb][key][ob]}\n')
                elif key == 'sub_transaction2':
                    for ob in log[arrayOb]['sub_transaction2']:
                        f.write(f'\t{ob}:\t{log[arrayOb][key][ob]}\n')
                else:
                    f.write(f'\t{log[arrayOb][key]}\n')
                    # for ob in App.log[arrayOb]['before_image']:
                    #    print("\t",App.log[arrayOb]['before_image'][ob])
                counter += 1
            count+= 1


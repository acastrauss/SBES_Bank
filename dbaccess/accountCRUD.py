import psycopg2
#from Certificate import Certificate
from config import config


def insertAccount(account,user):
    postgres_insert=""" INSERT INTO public.account(
	accountbalance, accountnumber, blocked, currency, datecreated, clientid, maintenancecost)
	VALUES ( %s, %s, %s, %s, %s,%s, %s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(postgres_insert, (account.accountBalance,account.accountNumber,account.blocked,account.currency,account.dateCreated,user.id,account.maintenanceCost),)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def checkAccNum(accountNumber):
    postgres_accnum=""" SELECT * FROM account 
    WHERE accountnumber = %s"""
    conn = None
    accnum = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        
        cur.execute(postgres_accnum,[accountNumber],)
        
        accnum = cur.fetchone()
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    try:
        if len(accnum)!=0:
            return True
        else: 
            return False
    except (Exception, psycopg2.DatabaseError) as error:
        return False


def checkAccCurrency(accountNumber):
    postgres_accnum=""" SELECT currency FROM account 
    WHERE accountnumber = %s"""
    conn = None
    acccur = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        
        cur.execute(postgres_accnum,[accountNumber],)
        
        acccur = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    try:
        if len(acccur[0])!=0:
            return acccur
        else: 
            return False
    except (Exception, psycopg2.DatabaseError) as error:
        return False
  
def updateAccBalance(accountid,acbal):
    postgres_accbal = """UPDATE public.account
	SET accountbalance = %s
    WHERE accountnumber = %s;"""
    conn = None
    updated_rows = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        
        cur.execute(postgres_accbal,(acbal,accountid,))  #(account.accountBalance,account.id,))
        
        updated_rows = cur.rowcount
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return updated_rows
  



if __name__ == '__main__':
    
   # c = Certificate('ss','ss','ss','ss','ss')
    #insertCert(c,22)
   print(checkAccNum(1111)) 
   print(checkAccCurrency(1111))
   print(updateAccBalance(1111,1389))

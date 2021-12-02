#!/usr/bin/python
import psycopg2
#from Certificate import Certificate
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insertCert(cert,user):
    postgres_insert=""" INSERT INTO public.certificate(
	cerpath, pfxpath, pvkpath, userid, authorityname, certificatename)
	VALUES ( %s, %s, %s, %s, %s, %s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(postgres_insert, (cert.cerPath,cert.pfxPath,cert.pvkPath,user.id,cert.authorityName,cert.certificateName,))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def getCertByUserId(userid):
    postgres_username=""" SELECT * FROM certificate WHERE userid = %s"""
    conn = None
    cert = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        
        cur.execute(postgres_username,(userid,))
        
        cert = cur.fetchall()
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return cert 



if __name__ == '__main__':
    
   # c = Certificate('ss','ss','ss','ss','ss')
    #insertCert(c,22)
   print(getCertByUserId(1)) 

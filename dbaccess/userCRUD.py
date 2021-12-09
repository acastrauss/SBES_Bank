#!/usr/bin/python
import psycopg2
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


def insertUser(userr):
    postgres_insert=""" INSERT INTO public.userr(
        birthdate, email, fullname, gender, jmbg, password, username, usertype)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(postgres_insert, (userr.birthdate,userr.email,userr.fullname,userr.gender,userr.jmbg,userr.password,userr.username,userr.usertype,))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def getAllUsers():
    postgres_allusers=""" SELECT * FROM userr """
    conn = None
    users = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        
        cur.execute(postgres_allusers,)
        
        users = cur.fetchall()
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return users

def getUserByUsername(username):
    postgres_username=""" SELECT * FROM userr WHERE username = %s"""
    conn = None
    usernm = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        
        cur.execute(postgres_username,(username,))
        
        usernm = cur.fetchall()
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return usernm

def getUserByJMBG(jmbg):
    postgres_jmbg=""" SELECT * FROM userr WHERE jmbg = %s"""
    conn = None
    jmbgg = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        
        cur.execute(postgres_jmbg,(jmbg,))
        
        jmbgg = cur.fetchall()
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return jmbgg

def getUserByEmail(mail):
    postgres_email=""" SELECT * FROM userr WHERE email = %s"""
    conn = None
    email = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        
        cur.execute(postgres_email,(mail,))
        
        email = cur.fetchall()
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    return email

def checkAvailability(username, email, jmbg):
    returnval = ''
    if len(getUserByJMBG(jmbg))!=0:
        returnval+='User with that jmbg already exists\n'
    if len(getUserByEmail(email))!=0:
        returnval+='User with that email already exists\n'
    if len(getUserByUsername(username))!=0:
        returnval+='User with that username already exists'

    if(returnval==''):
        returnval=True
    return returnval

def login(username, password):
    postgres_login=""" SELECT * FROM userr WHERE username = %s and password = %s"""
    conn = None
    login = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        
        cur.execute(postgres_login,(username,password))
        
        login = cur.fetchall()
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    if len(login)!=0:
        return True
    else: 
        return False
if __name__ == '__main__':
    connect()
  #  niz = getAllUsers()
   # for data in niz:
    #    print(data)

    ##korisnik = getUserByUsername('probni2sssr')
    #print(korisnik)
    ##print(len(getUserByJMBG('12345674432111')))
    #print(getUserByEmail('proba@sssr.ru'))
    print(login('kossrisnikk','asdfghjk'))
    #print(checkAvailability('skorisnikk','sproba@sssr.ru','s123456744321'))
    
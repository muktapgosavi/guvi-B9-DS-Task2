from codecs import register
import mysql.connector
import re

hostname = '127.0.0.1'
username = 'MySQL8'
password = 'MysqlRoot@123'
database = 'pythonlogin'


#import mysql.connector
myConnection = mysql.connector.connect( host=hostname, user=username, passwd=password, db=database, auth_plugin='mysql_native_password' )
cur = myConnection.cursor(prepared=True)

def Register():
    username = input("Name : ")
    email = input("Email id : ")
    pass1 = input("Enter Password : ")
    pass2 = input("Enetr Password again : ")

    cur.execute('SELECT * FROM accounts WHERE username = %s', (username,))
    account = cur.fetchone()
    if account:
        print('Account already exists!')
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print('Invalid email address!')
    elif not re.match(r'[A-Za-z0-9]+', username):
        print('Username must contain only characters and numbers!')
    elif not pass1 == pass2:
        print('Password dose not matched! Enter the password again.')
    elif not username or not pass1 or not email:
        print('Please fill out the form!')
    else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
        cur.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, pass1, email,))
        myConnection.commit()
        print('You have successfully registered!')


def login():
    username = input("Name : ")
    password = input("Enter Password : ")

    cur.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
    account = cur.fetchone()
    myConnection.commit()
    # If account exists in accounts table in out database
    if account :
        print("-------Logged in successfully!---------")
        return'Logged in successfully!'
    else:
        # Account doesnt exist or username/password incorrect
        print('Incorrect username/password!')
        return 1


def forgot_password():
    name = input("Enter your username : ").lower()
    try:
        password = cur.execute("SELECT password FROM accounts WHERE username = '"+name+"'").lower()
        if (password):
            print("Your password : '"+password+"'")
            myConnection.commit()
        else:
            print("Username Not Found! \n Please Register Yourself..")
            register()
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)

    finally:
        if myConnection.is_connected():
            myConnection.close()
            cur.close()
            print("MySQL connection is closed")

        



while(True):
    acc = input("Do You have an Account? \n(Please Enter Yes or No)\n(-Press 0 to exit-): ").lower()

    if acc == 'yes' :
        a = login()
        if a == 1:
            op = input("Forgot Password? : \n(Please Enter yes or no)").lower()
            if op == 'yes':
                forgot_password()
            else:
                login()
        else :
            print(a)          
        pass        

    elif acc == 'no':
        print("Please Register yourself first...!")
        Register()    
        pass

    else:
        print("Thank You!")
        break
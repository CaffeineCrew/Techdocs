from dotenv import load_dotenv
load_dotenv()
import os

import mysql.connector
from mysql.connector import errorcode

config={
    'host':os.environ.get("HOSTNAME"),
    'user':os.environ.get("UID"),
    'password':os.environ.get("PASSWORD"),
    'database':os.environ.get("DATABASE")
}

print(config)

try:
    cnx = mysql.connector.connect(**config)
    print("Connection established")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = cnx.cursor()

    cursor.execute("DROP TABLE IF EXISTS api_key")
    cursor.execute("DROP TABLE IF EXISTS auth")
    cursor.execute("CREATE TABLE IF NOT EXISTS auth(username VARCHAR(15) PRIMARY KEY, password TEXT, email VARCHAR(50))")
    cursor.execute("CREATE TABLE IF NOT EXISTS api_key(username VARCHAR(15),apikey TEXT, FOREIGN KEY (username) REFERENCES auth(username))")
    cursor.execute("ALTER TABLE auth ADD is_verified BOOLEAN NOT NULL DEFAULT(false)")

    # QUERY = ('INSERT INTO {coll_name} '
    #                 '(username, password, email) '
    #                 'VALUES '
    #                 '(%s, %s, %s)').format(coll_name="auth")

    # testlist=[("test2","test2","test2@test.com"),("test1","test1","test1@test1.com")]
    # cursor.executemany(QUERY, testlist)

    # QUERY = ('SELECT {cols} FROM {table_name} WHERE email="test2@test.com"').format(cols="*", table_name="auth")
    # cursor.execute(QUERY)
    # for i in cursor.fetchall():
    #     print(i)




    cnx.commit()
    cursor.close()
    cnx.close()
# from jose import jwt
# print(jwt.encode("bruhh"))

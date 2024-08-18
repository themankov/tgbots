import sqlite3
import os

directory = os.path.join(os.path.dirname(__file__), '..', 'db', 'users.db')
async def selectUserById(userId):
 
    conn=sqlite3.connect(directory) 
    cursor=conn.cursor()
    cursor.execute('''
    SELECT * FROM users 
    WHERE userId=?           
''',(userId,))
    rows=cursor.fetchall()
    return rows
async def addUserToDB(userId,username,name,age,city):
  conn=sqlite3.connect(directory)
  cursor=conn.cursor()
  cursor.execute('''
    INSERT INTO users (userId, username,name, age, city)
    VALUES (?, ?, ?, ?, ?)
    ''', (userId,username,name, age, city))

  conn.commit()
  conn.close()
async def deleteUserFromDb(userId):
  conn=sqlite3.connect(directory)
  cursor=conn.cursor()
  cursor.execute('''
    DELETE FROM users
    WHERE userId=?
    ''',(userId,))

  conn.commit()
  conn.close()
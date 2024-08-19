from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Создание базы данных и подключение к ней
DATABASE_URL = 'postgresql://postgres:123456@localhost:5432/tgbot'
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'Users'

    userId = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    city = Column(String, nullable=False)

    # Свойство plans доступно у каждого User, получение всех объектов Plan
    plans = relationship("Plan", back_populates="user")

class Plan(Base):
    __tablename__ = 'Plans'

    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    content = Column(String, nullable=False)
    userId = Column(BigInteger, ForeignKey('Users.userId'))
    finished = Column(Boolean, default=False, nullable=False)

    # Связь с таблицей User
    user = relationship("User", back_populates="plans")


Base.metadata.create_all(engine)




# import sqlite3
# import os

# directory = os.path.join(os.path.dirname(__file__), '..', 'db', 'users.db')
# async def selectUserById(userId):
 
#     conn=sqlite3.connect(directory) 
#     cursor=conn.cursor()
#     cursor.execute('''
#     SELECT * FROM users 
#     WHERE userId=?           
# ''',(userId,))
#     rows=cursor.fetchall()
#     return rows
# async def addUserToDB(userId,username,name,age,city):
#   conn=sqlite3.connect(directory)
#   cursor=conn.cursor()
#   cursor.execute('''
#     INSERT INTO users (userId, username,name, age, city)
#     VALUES (?, ?, ?, ?, ?)
#     ''', (userId,username,name, age, city))

#   conn.commit()
#   conn.close()
# async def deleteUserFromDb(userId):
#   conn=sqlite3.connect(directory)
#   cursor=conn.cursor()
#   cursor.execute('''
#     DELETE FROM users
#     WHERE userId=?
#     ''',(userId,))

#   conn.commit()
#   conn.close()
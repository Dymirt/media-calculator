import sqlite3
from sqlite3 import Error

database_file = 'utility.db'

sql_create_table_list = [
    """ CREATE TABLE IF NOT EXISTS utilities (
                                    UtilityId INTEGER PRIMARY KEY,
                                    Name TEXT NOT NULL,
                                    Symbol TEXT,
                                    Price REAL NOT NULL,
                                    SubscriptionPrice REAL  
                                ); """,
    """ CREATE TABLE IF NOT EXISTS history (
                                    Id INTEGER PRIMARY KEY,
                                    Date TEXT NOT NULL,
                                    UtilityId INTEGER NOT NULL,
                                    Price REAL NOT NULL,
                                    SubscriptionPrice REAL,
                                    Value REAL NOT NULL,
                                    Consumption REAL NOT NULL,
                                    Payment REAL NOT NULL,
                                    
                                    FOREIGN KEY (utilityId)
                                        REFERENCES utilities (utilityId) 
                                ); """

]

sql_add_utility = 'INSERT INTO utilities (Name, Symbol, Price, SubscriptionPrice) values(?, ?, ?, ?)'
# sql_add_history = #TODO qurey add_history


DATABASE = sqlite3.connect(database_file)
cur = DATABASE.cursor()
for sql in sql_create_table_list:
    cur.execute(sql)


def add_utility(utility: tuple):
    try:
        DATABASE.cursor().execute(sql_add_utility, utility)
        DATABASE.commit()
    except Error as e:
        print(e)


def get_all_utilities():
    c = DATABASE.cursor()
    c.execute('SELECT * FROM utilities')
    return c.fetchall()


def get_all_utility_name():
    c = DATABASE.cursor()
    c.execute('SELECT UtilityId, name FROM utilities')
    utility_names_list = {}
    for i in c.fetchall():
        utility_names_list[i[0]] = i[1]
    print(utility_names_list)
    return utility_names_list


def set_utilities():
    utility_list = [
        ("Electricity", "kW⋅h", 0.481053, 21.98),
        ("Cold Water", "m³", 9.85, 0),
        ("Hot water", "m³", 9.85 + 20.61, 0)
    ]
    DATABASE.cursor().executemany(sql_add_utility, utility_list)
    DATABASE.commit()


def get_values_by_name(name):
    c = DATABASE.cursor()
    c.execute('SELECT price, SubscriptionPrice FROM utilities WHERE Name=?', (name,),)
    return c.fetchone()

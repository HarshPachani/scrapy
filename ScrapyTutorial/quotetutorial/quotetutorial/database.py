#Manually Created by Harsh Pachani.
import sqlite3

conn = sqlite3.connect("myquotes.db")
curr = conn.cursor()

curr.execute("""CREATE TABLE IF NOT EXISTS quotes_db(
    title TEXT,
    author TEXT,
    tag TEXT
    )""")

curr.execute("""INSERT INTO quotes_db VALUES('Python is awesome!', 'buildwithpython', 'python')""")

conn.commit()
conn.close()
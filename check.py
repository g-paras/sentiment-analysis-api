import sqlite3 as sql
con = sql.connect("text.sqlite")
con.row_factory = sql.Row

cur = con.cursor()
cur.execute("select * from Texts")

rows = cur.fetchall(); 
con.close()
for row in rows:
    print(row["id"], row["text"], row["date"], row["sentiment"])
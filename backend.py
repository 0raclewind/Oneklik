import sqlite3


def connect():
	conn = sqlite3.connect("data.db")
	cur = conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, name text, user_id text, pwd text, answer1 text, answer2 text, answer3 text)")
	conn.commit()
	conn.close()


def register(name, user_id, pwd, answer1, answer2, answer3):
	conn = sqlite3.connect("data.db")
	cur = conn.cursor()
	cur.execute("INSERT INTO accounts VALUES (NULL,?,?,?,?,?,?)", (name, user_id, pwd, answer1, answer2, answer3))
	conn.commit()
	conn.close()


def view():
	conn = sqlite3.connect("data.db")
	cur = conn.cursor()
	cur.execute("SELECT * FROM accounts")
	rows = cur.fetchall()
	conn.close()
	return rows


def delete(name):
	conn = sqlite3.connect("data.db")
	cur = conn.cursor()
	cur.execute("DELETE FROM accounts WHERE name=?", (name,))
	conn.commit()
	conn.close()


def get_user_info(name):
	conn = sqlite3.connect("data.db")
	cur = conn.cursor()
	cur.execute("SELECT * FROM accounts WHERE name=?", (name,))
	account = cur.fetchall()[0]
	conn.close()
	return account

connect()

#!/usr/bin/python
#################
# Cmdiary v 1.0 #################################
# A simple command line diary/agend/notes keeper#
# or whatever you want to use it for.           #
# It is based on a sqlite database.             #
# Just few hours was spent on this, but any     #
# suggestion, comment improvement or report will#
# be happily appreciated.                       #
# copyleft joker__<g.chers@gmail.com>           #
#################################################
# file: diary.py
# desc: sqlite database handler
import sqlite3
import datetime


class diary:
	def __init__(self, dbname, username, userbirthday=''):
		'''Inits the db connection.'''
		self.user  = username
		self.birth = userbirthday
		self.conn  = self.connect(dbname)
		if not self.conn:
			raise Exception('DB error.')
		id = self.get_userid(username)
		if id < 0:
			self.create_user(username, userbirthday)
			id = self.get_userid(username)
		self.id = id
		
	def __exit__(self):
		'''Close the db connection on object destruction.'''
		self.conn.close()	
	
	def check_db(self, conn):
		'''Executes simple queries to db, in order
		to verify if the needed tables are present.'''
		try:
			conn.execute('SELECT * FROM user')
			conn.execute('SELECT * FROM note')
			return True
		except sqlite3.Error, e:
			return False
	
	def connect(self, dbname):
		'''Connects and test if the database is
		properly configured.'''
		conn = sqlite3.connect(dbname) # if db doesn't exist it creates a new one
		if not self.check_db(conn):
			self.create_db(conn)
			if not self.check_db(conn):
				return False
		return conn
	
	def create_db(self,conn):
		'''Creates the tables on the given sqlite
		db connection.'''
		# Note: on sqlite "rowid" is automatically created.
		# 		It will be our primary key.
		try:
			conn.execute('''CREATE TABLE user (name VARCHAR(45)
			UNIQUE NOT NULL, birthday DATE NULL)''')
		
			conn.execute('''CREATE TABLE note (title VARCHAR(45)
			NULL, content VARCHAR(500) NULL, writing_date DATETIME
			NULL, event_date DATETIME NULL, user_id INT NOT NULL)''')
			conn.commit()
		except sqlite3.OperationalError:
			pass # eg a table already exists...no problem
		except:
			raise
	
	def create_user(self, username, userbirthday):
		'''Inserts a new user into the database.'''
		self.conn.execute('''INSERT INTO user VALUES (?, ?)''',
		(username, userbirthday,))
		self.conn.commit()
		
	
	def get_events(self, date=''):
		'''Returns all events of the given date. If no date
		is given, today's events are returned.'''
		if date == '':
			date = datetime.datetime.now().strftime("%Y-%m-%d")+'%'
		c = self.conn.cursor()
		c.execute('SELECT * FROM note WHERE rowid = ? AND event_date LIKE ?', (self.id,date,))
		return c.fetchall()
	
	def get_userid(self, username):
		'''Returns the id of the given user. If the user does
		not exist, it returns -1'''
		c = self.conn.cursor()
		c.execute('SELECT rowid FROM user WHERE name = ?', (username,))
		id = c.fetchone()
		if not id:
			return -1
		return int(id[0])
	
	def new_event(self, title, content, event_date='', event_time='', date='date("now")', time='time("now")'):
		'''Insert a new event in the calendar. Date and time
		represent the day of writing, and are set by default.'''
		date += ' '+time
		if event_time != '':
			event_date += ' '+event_time
		try:
			self.conn.execute('INSERT INTO note VALUES (?,?,?,?,?)',
			(title, content, date, event_date, self.id,))
			self.conn.commit()
			return True
		except:
			return False
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


class note:
	#### warning: no check if init fails
	def __init__(self, title, content=0, writing_date=0, event_date=0):
		self.title = ''
		self.content = ''
		self.writing_date = ''
		self.event_date = ''
		# content=0 -> a touple is given, on "title" variable
		if content==0:
			if len(title) >= 4:
				self.title = title[0]
				self.content = title[1]
				self.writing_date = title[2]
				self.event_date = title[3]
		else:
			self.title = title
			self.content = content
			self.writing_date = writing_date
			self.event_date = event_date


class diary:
	def __init__(self, dbname, username, userbirthday=''):
		'''Inits the db connection.'''
		self.user  = username
		self.birth = userbirthday
		self.conn  = self.connect(dbname)	# gives a connection to the sqlite db
		if not self.conn:
			raise Exception('DB error.')
		self.cursor= self.conn.cursor()		# for fetching sqlite's statements results
		
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
		except sqlite3.Error as e:
			print e
			return False
	
	
	def connect(self, dbname):
		'''Connects and test if the database is
		properly configured.'''
		# if dbname db doesn't exist it creates a new one
		conn = sqlite3.connect(dbname, check_same_thread = False)
		# if db is not properly structured, it inits its tables' columns
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
		
	
	def get_notes(self, type, date=''):
		'''Returns all events programmed for the given date (type='p'),
		or all the events written on the indicated date (type='w'). If
		no date is given, today's events/written events are returned.'''
		if date == '':
			date = '"'+datetime.datetime.now().strftime("%Y-%m-%d")+'%"'
		else:
			date ='"'+date+'%"'
		if type == 'e':
			type = 'event_date'
		elif type == 'w':
			type = 'writing_date'
		else:
			return
		
		self.cursor.execute('SELECT * FROM note WHERE  user_id = ? AND ? LIKE ?', (self.id,type,date,))
		r = []
		for n in self.cursor.fetchall():
			r.append(note(n))
		return r
	
	
	def get_userid(self, username):
		'''Returns the id of the given user. If the user does
		not exist, it returns -1'''
		self.cursor.execute('SELECT rowid FROM user WHERE name = ?', (username,))
		id = self.cursor.fetchone()
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
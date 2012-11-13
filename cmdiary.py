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
# file: cmdiary.py
# desc: the main class, which handles the command
#       line UI and the diary itself

# TODO:
# 	* indented blocks
#	* language
#	* try on import
#
import datetime
import threading
from diary import diary


class cmdiary(threading.Thread):
	'''Handles a diary objects, with a
	non graphic UI.'''
	def __init__(self, dbname, username):
		threading.Thread.__init__(self)
		try:
			self.diary = diary(dbname, username)
		except:
			print 'SQLite error: do you have sqlite3 installed?' #asdfasfsadf
			exit(0)
	
	def prompt(self):
		'''Simply prompts all today's events
		and then quits.'''
		print '-'*24
		print 'Che succede oggi?'
		print '-'*24
		for evt in self.diary.get_events():
			self.print_event(evt)
	
	def print_event(self,evt):
		'''Prints a event/note.'''
		if len(evt) < 4:
			return
		print 'title:',str(evt[0]).strip()
		print 'content:',str(evt[1]).strip()
		print 'at:',str(evt[2]).strip()
		print 'written:',str(evt[3]).strip()
		print
		
	def run(self):
		'''UI'''
		self.running = True
		#while self.running:
		# functions:
		#	* date events
		#	* calendar (cal)
		#	* insert event
		#	* delete event
		#	* delete all events ?
		#	* show all events (sure?)
		#	* exit
		#	* chose language


dbname = 'cmdiary.db'
username = 'Giovanni'
cmdiary = cmdiary(dbname, username)
cmdiary.prompt()		
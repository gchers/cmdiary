#!/usr/bin/python
#################
# Cmdiary v 0.1 #################################
# A simple command line diary/agend/notes keeper#
# or whatever you want to use it for.           #
# It is based on a sqlite database.             #
# Just few hours was spent on this, but any     #
# suggestion, comment improvement or report will#
# be happily appreciated.                       #
# Copyleft joker__<g.chers@gmail.com>           #
#################################################
# file: cmdiary.py
# desc: the main class, which handles the command
#       line UI and the diary itself

# TODO:
#	* language
#	* delete events-notes
#
# *** get_notes???

import datetime
import threading
import show
import sys
from diary import diary


class cmdiary(threading.Thread):
	'''This is the main class. Handles a diary objects,
	and uses show.py to show the contents to the user
	by a non graphic UI.'''
	def __init__(self, dbname, username):
		threading.Thread.__init__(self)
		try:
			self.diary = diary(dbname, username)
		except Exception as e:
			print e
			exit(0)
	
	def goto_date(self, type):
		'''Asks for what date-date range search for and shows
		all events of that day.'''
		date = show.calendar()

		if date:
			for evt in self.diary.get_notes('e', date):
				show.print_event(evt)
		else:
			self.help()
	
	def goto_event(self):
		self.goto_date('e')
	

	def goto_note(self):
		self.goto_date('w')
	
	def new_note(self):
		'''Insert a new note.'''
		title = raw_input('Title: ')
		content = raw_input()
		print 'Are you going to associate it to a date? Set a date! (else just "Enter")' # time?
		evt_date = show.calendar()
		if self.diary.new_event(title, content, evt_date):
			print 'Your note was added.'
		else:
			print 'Something were wrong...so sorry man.'
	

	def help(self):
		print 'help'
		
	def prompt(self):
		'''Simply prompts all today's events
		and then quits.'''
		print 'What\'s happening today?'
		for evt in self.diary.get_notes('e'):
			show.print_event(evt)
		
	def run(self):
		'''UI'''
		# The following statement "functions[s]()" referred to the
		# array "functions", emulates a switch/case-of
		# under Python. It is a really nice piece of code, and here
		# is where I got it from:
		# http://simonwillison.net/2004/may/7/switch/
		#
		functions = {
				'?' : ("cannot call this directly", 'Show this help.'),
				'p' : (self.prompt, 'Prompt. This is the default function: it shows all the events programmed for today.'),
				'e' : (self.goto_event, 'Show all the events programmed for one day.'),
				'w' : (self.goto_note, 'Show all the notes-events written on the specified date.'),
				'n' : (self.new_note, 'Create a new note-event.'),
				'x' : (self.stop, 'Exit from diary.')
				}
		
		show.welcome()
		
		self.running = True
		while self.running:
			try:
				s = raw_input("> ");
				if s == '?':
					show.functions_help(functions)
				else:
					functions[s][0]()
			except EOFError:
				exit(0)
			except Exception as e:
				show.functions_help(functions)
				#print e
				pass
	
	def stop(self):
		'''Ends the while cycle if running.'''
		self.running = False


if __name__ == "__main__":
	dbname = 'cmdiary.db'
	username = 'Giovanni'
	try:
		cmdiary = cmdiary(dbname, username)
	except:
		print 'Error when creating a database in path', dbname,'.'
		exit(-1)
	
	if len(sys.argv) > 1:
		if sys.argv[1] == '-i': 	# interactive mode
			cmdiary.start()
		else:
			print 'fuck.'      #adsfhasufguwqgfiuqwjebfkjqwbfkwjebfkjqwb
	else:
		cmdiary.prompt() 		# just prompt today's events

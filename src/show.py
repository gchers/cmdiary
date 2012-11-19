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
# file: show.py
# desc: non graphic UI. Interfaces with cmdiary.py
#		and show informations to the user.
import os
from diary import note

try:
	rows, columns = os.popen('stty size', 'r').read().split()
	columns = int(columns)
except: # should it fail on Windows? I don't know it
	columns = 0

def calendar():
	'''Requires to run on Unix system with cal installed.'''
	date = '?'
	while date.startswith('?'):
		date = raw_input("Date [YYYY-mm-dd] (\"? <month/year>\" for calendar): ")
		if date.startswith('?'):
			try:
				print
				os.system("cal " + date.replace('?','').strip())
				print
			except Exception as e:
				print 'Not (yet) supported on your OS. If you\'re using Unix-Linux check if "cal" is installed'
				print e
	return date


def functions_help(functs):
	'''Takes a "functions" dictionary, defined into diary.py, which
	is composed as:
	'choice char': (associated function, function explanation string)
	and prints a help based on these informations.'''
	print 'HELP'
	for k in functs.keys():
		if len(functs[k]) == 2:
			print indent(k+': '+functs[k][1], 3)


# Note: maybe a better algorithm for doing this exists...
# 		not a really nice code.
def indent(text, n, first_line=True):
	'''Indents a paragraph of n spaces. If first_line enabled, the
	first line is not indented. '''
	global columns
	#columns = 10
	if columns ==0:
		return text
	c=len(text)/columns
	if c == 0:
		return text
	str = ''
	start = 0
	if first_line:
		str += text[0: columns] + '\n'
		start = columns
	i=start
	for i in range(start, c*columns, columns):
		str += ' '*n + text[i:i+columns] + '\n'
	str += ' '*n + text[-(len(text)%columns):] # remaining characters
	return str


# Note: there is no difference between a note and a
#		event. They're both "diary.note" objects.
#		Btw there are two different way of printing
#		their content: print_note, print_event.
def print_note(note):
	'''Prints a note.'''
	print indent('Title:   '+ note.title.strip()+' - '+note.writing_date.strip(),9)
	print indent('Content: '+ note.content.strip(),9)
	
def print_event(evt):
	'''Prints a event.'''
	print indent('Title:   '+ evt.title.strip(),9)
	print indent('Content: '+ evt.content.strip(),9)
	print indent('At:      '+ evt.event_date.strip(),9)
	print indent('Written: '+ evt.writing_date.strip(),9)
	
	
def welcome():
	'''Info about the program/version.'''
	intro = '''A simple command line diary/agend/notes keeper or whatever you want to use it for. If you don't know where to start from, '?' will display you the contextual help. \nCopyleft joker__<g.chers@gmail.com>'''
	
	#print
	print 'Cmdiary version 0.1. Type \'?\' for help.'
	#print intro

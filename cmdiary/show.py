#!/usr/bin/python
#################
# Cmdiary v 0.1 #################################
# A simple command line diary/agend/notes keeper#
# or whatever you want to use it for.           #
# It is based on a sqlite database.             #
# Few hours was spent on this, and any			#
# suggestion, comment improvement or fix will	#
# be really appreciated.                        #
# If you want to contribute, first look at the	#
# TODO file.									#
#												#
# Copyleft joker__<g.chers@gmail.com>           #
#################################################
# file: show.py
# desc: non graphic UI. Interfaces with cmdiary.py
#		and show informations to the user.
import os
#from cmdiary import *
from diary import note

version = 'Cmdiary version 0.1.'

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
	print 'Help'
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
		str += text[0: columns].strip() + '\n'
		start = columns
	i=start
	for i in range(start, c*columns, columns):
		str += ' '*n + text[i:i+columns].strip() + '\n'
	str += ' '*n + text[-(len(text)%columns):].strip() # remaining characters
	return str


def help(flags):
	'''This is the main help. Explains what the flags do.'''
	print version
	print 'usage: cmdiary [options]'
	print 'Options:'
	for k in flags.keys():
		if len(flags[k]) == 2:
			print indent(k+': '+flags[k][1], 8)

# Note: there is no difference between a note and a
#		event. They're both "diary.note" objects.
#		Btw there are two different way of printing
#		their content: print_note, print_event.
def print_note(note):
	'''Prints a note.'''
	print indent('Title:   '+ str(note.title).strip()+' - '+note.writing_date.strip(),9)
	print indent('Content: '+ str(note.content).strip(),9)
	
def print_event(evt):
	'''Prints a event.'''
	print indent('Title:   '+ str(evt.title).strip(),9)
	print indent('Content: '+ str(evt.content).strip(),9)
	print indent('At:      '+ str(evt.event_date).strip(),9)
	print indent('Written: '+ str(evt.writing_date).strip(),9)
	
	
def welcome():
	'''Info about the program/version.'''
	intro = '''A simple command line diary/agend/notes keeper or whatever you want to use it for. If you don't know where to start from, '?' will display you the contextual help. \nCopyleft joker__<g.chers@gmail.com>'''
	
	#print
	print version + ' Type \'?\' for help.'
	#print intro

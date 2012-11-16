from diary import note


# Note: there is no difference between a note and a
#		event. They're both "diary.note" objects.
#		Btw there are two different way of printing
#		their content: print_note, print_event.
def print_note(note):
	'''Prints a note.'''
	print 'title:  ', note.title.strip(),'-',note.writing_date.strip()
	print 'content:', note.content.strip()
	
def print_event(evt):
	'''Prints a event.'''
	print 'title:  ', evt.title.strip()
	print 'content:', evt.content.strip()
	print 'at:     ', evt.event_date.strip()
	print 'written:', evt.writing_date.strip()
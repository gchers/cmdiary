import os
from setuptools import setup, find_packages

#sources = ['cmdiary.py','diary.py','show.py']
#srcdir  = './src/'
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup (
	name			= 'CMDiary',
	version 		= '0.1',
	author 			= 'Giovanni Cherubin (joker__)',
	author_email 	= 'g.chers@gmail.com',
	description 	= 'A simple command line diary/agend/notes keeper or whatever you want to use it for.',
	license 		= 'GPLv2',
	keywords 		= 'diary agend terminal notes',
	long_description= read('README'),
	classifiers		= ["Development Status :: 4 - Beta",
					"Topic :: Utilities",
					"License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
					"Environment :: Console",],
	
	packages = ['cmdiary',],
	scripts = ['cmdiary/cmdiary']	
)

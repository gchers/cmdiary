from setuptools import setup

sources = ['cmdiary.py','diary.py','show.py']
srcdir  = './src/'

setup (
	name = 'CMDiary',
	version = '0.1',
	author = 'Giovanni Cherubin joker__',
	author_email = 'g.chers@gmail.com',
	description = 'A simple command line diary/agend/notes keeper or whatever you want to use it for.',
	license = 'GNU GPL',
	keywords = 'diary, agent, command line',
	long_description=read('README'),
	classifiers=["Development Status :: 4 - Beta",
				"Topic :: Utilities",
				"License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
				"Environment :: Console"]
	
	entry_points = {
        "console_scripts": [
            "cmdiary": "cmdiary:main",
        ],
    }

)

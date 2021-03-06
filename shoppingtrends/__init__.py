"""
The Main Program

This is the file that will be run when the application is started. 
Its function is to connect all the pieces of the application so that we 
end up with a useful piece of software.
"""

import os.path
from database import db_init
from data import populate_all_tables
from authorization import Authorzation
from application import Root
from user import User

db_exists = os.path.isfile('test.db')

db = 'sqlite:///:memory:'
#db = 'sqlite:///test.db'

session = db_init(db)

if not db_exists:
    populate_all_tables(session)

#login = Authorzation(session)
#login.mainloop()


#temporary, will be used until application is in a more complete state
session_user = session.query(User).filter_by(username='jhooey').first()


#Main Application
root = Root(session_user, session)
root.mainloop()

try:
    session_user = login.session_user
    login.destroy()
except: 
    quit()

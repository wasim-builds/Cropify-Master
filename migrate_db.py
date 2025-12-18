from App import app, db
from Models import *

with app.app_context():
    db.drop_all()
    db.create_all()
    print('Database recreated with new schema!')

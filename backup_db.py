#!flask/bin/python
import app
from app import db, models
from app.models import Character, Suggestion

f = open('backupfile', 'r+')

for char in Character.query.all():
	f.write(char.name)
	f.write("\n")

f.close()

#!flask/bin/python
import app
from app import db, models
from app.models import Character, Move

w = Character.query.filter_by(name='wolf').first()
for m in w.moves:
	db.session.delete(m)
	db.session.commit()

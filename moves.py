#!flask/bin/python
import app
from app import db, models
from app.models import Character, Move

w = Character.query.filter_by(name='wolf').first()
f = open('lists/wolf', 'r')
for line in f:
	d = line.split()
	if "Air" in d[0]:
		m = Move(w.id, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10])
		m.landing=d[11]
		m.auto=d[12]
	else:
		m = Move(w.id, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10])
		m.onhit=d[11]
	db.session.add(m)
	db.session.commit()
f.close()
	
y = Character.query.filter_by(name='yoshi').first()
f = open('lists/yoshi', 'r')
for line in f:
	d = line.split()
	if "Air" in d[0]:
		m = Move(y.id, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10])
		m.landing=d[11]
		m.auto=d[12]
	else:
		m = Move(y.id, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10])
		m.onhit=d[11]
	db.session.add(m)
	db.session.commit()
f.close()

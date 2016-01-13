#!flask/bin/python

import app
from app import models, db
from app.models import Character, Smashup

chars = ["Bowser", "Captain Falcon", "Charizard", "Diddy Kong", "Donkey Kong", "Falco", "Fox", "Mr. Game & Watch", "Ganondorf", "Ice Climbers", "Ike", "Ivysaur", "Jigglypuff", "King Dedede", "Kirby", "Link", "Lucario", "Lucas", "Luigi", "Mario", "Marth", "Meta Knight", "Mewtwo", "Ness", "Olimar", "Peach", "Pikachu", "Pit", "R.O.B.", "Roy", "Samus", "Sheik", "Snake", "Sonic", "Squirtle", "Toon Link", "Wario", "Wolf", "Yoshi", "Zelda", "Zero Suit Samus"]

for char in chars:
	safe = char.replace(" ", "")
	safe = safe.replace(".", "")
	safe = safe.replace("&", "and")
	c = Character(char.lower(), safe.lower())
	db.session.add(c)
	db.session.commit()

for name1 in chars:
	char1 = Character.query.filter_by(name=name1.lower()).first()
	print "+++%r+++" % char1.name
	for name2 in chars:
		char2 = Character.query.filter_by(name=name2.lower()).first()
		print "%r" % char2.name
		s = Smashup(char1.name, char2.name)
		print s
		db.session.add(s)
		db.session.commit()	

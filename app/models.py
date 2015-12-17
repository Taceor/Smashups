from app import db

class Character(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(25), unique=True)
	quick = db.Column(db.Text)
	depth = db.Column(db.Text)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Character %r>' % (self.name.encode('utf8'))

class Smashup(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	char = db.Column(db.String(25), db.ForeignKey('character.name'))
	oppo = db.Column(db.String(25), db.ForeignKey('character.name'))
	pros = db.relationship('Pro', backref='smashup', lazy='dynamic')
	cons = db.relationship('Con', backref='smashup', lazy='dynamic')
	neut = db.relationship('Neutral', backref='smashup', lazy='dynamic')
	
	def __init__(self, char, oppo):
		self.char = char
		self.oppo = oppo

	def __repr__(self):
		return '<Smashup %r vs %r>' % (self.char, self.oppo)

class Pro(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(140))
	smashup_id = db.Column(db.Integer, db.ForeignKey('smashup.id'))

	def __init__(self, text, smashup_id)
		self.text = test
		self.smashup_id = smashup_id

	def __repr__(self):
		return '<Pro %r: %r>' % (self.id, self.text[0:15])

class Con(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(140))
	smashup_id = db.Column(db.Integer, db.ForeignKey('smashup.id'))

	def __init__(self, text, smashup_id)
		self.text = test
		self.smashup_id = smashup_id

	def __repr__(self):
		return '<Con %r: %r>' % (self.id, self.text[0:15])

class Neutral(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(1000))
	smashup_id = db.Column(db.Integer, db.ForeignKey('smashup.id'))

	def __init__(self, text, smashup_id)
		self.text = test
		self.smashup_id = smashup_id

	def __repr__(self):
		return '<Neutral %r: %r>' % (self.id, self.text[0:15])

"""Class Suggestion
	id
	text
	score
	user = relationship
"""

"""Class User
	id
	name
	email
	hashword <-- figure out how to do safely
	is_admin
	comments = relationship
	messages_in = relationship
	messages_out = relationship
	suggestions = relationship
"""

"""Class Comment
	id
	text
	user = relationship
	parent <-- figure out some shiz
	time
"""

"""Class Message
	id
	from = relationship
	to = relationship
	unread
"""


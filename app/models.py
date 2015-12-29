from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Character(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(25), unique=True)
	quicks = db.relationship('Quick', backref='character', lazy='dynamic')
	depths = db.relationship('Depth', backref='character', lazy='dynamic')

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

class Quick(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(140))
	char_id = db.Column(db.Integer, db.ForeignKey('character.id'))

	def __init__(self, text, char_id):
		self.text = text
		self.char_id = char_id

	def __repr__(self):
		return '<Quick %r: %r>' % (self.id, self.text[0:15])

class Depth(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(140))
	char_id = db.Column(db.Integer, db.ForeignKey('character.id'))

	def __init__(self, text, char_id):
		self.text = text
		self.char_id = char_id

	def __repr__(self):
		return '<Depth %r: %r>' % (self.id, self.text[0:15])

class Pro(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(140))
	smashup_id = db.Column(db.Integer, db.ForeignKey('smashup.id'))

	def __init__(self, text, smashup_id):
		self.text = text
		self.smashup_id = smashup_id

	def __repr__(self):
		return '<Pro %r: %r>' % (self.id, self.text[0:15])

class Con(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(140))
	smashup_id = db.Column(db.Integer, db.ForeignKey('smashup.id'))

	def __init__(self, text, smashup_id):
		self.text = text
		self.smashup_id = smashup_id

	def __repr__(self):
		return '<Con %r: %r>' % (self.id, self.text[0:15])

class Neutral(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(1000))
	smashup_id = db.Column(db.Integer, db.ForeignKey('smashup.id'))

	def __init__(self, text, smashup_id):
		self.text = text
		self.smashup_id = smashup_id

	def __repr__(self):
		return '<Neutral %r: %r>' % (self.id, self.text[0:15])

class Suggestion(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	character = db.Column(db.String(42))
	opponent = db.Column(db.String(42))
	section = db.Column(db.String(42))
	text = db.Column(db.Text)
	score = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, character, text, user_id):
		self.character = character
		self.text = text
		self.user_id = user_id

	def __repr__(self):
		return '<Suggestion %r: %r, %r, %r>' % (self.id, self.user_id, self.character, self.text[0:15])

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(42))
	email = db.Column(db.String(255))
	password = db.Column(db.String(255))
	pw_hash = db.Column(db.String(255))
	about = db.Column(db.Text())
	main = db.Column(db.String(42))
	suggestions = db.relationship('Suggestion', backref='user', lazy='dynamic')
	
	def __init__(self, nickname, email, password):
		self.nickname = nickname
		self.email = email
		self.set_password(password)

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.nickname)

	"""
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
	topic
	time
"""

"""Class Message
	id
	from = relationship
	to = relationship
	unread
"""

from app import db
from werkzeug.security import generate_password_hash, check_password_hash

votes = db.Table('votes',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('suggestion_id', db.Integer, db.ForeignKey('suggestion.id')),
)

class Character(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(25), unique=True)
	safename = db.Column(db.String(25), unique=True)
	suggs = db.relationship('Suggestion', backref='character', lazy='dynamic')
	moves = db.relationship('Move', backref='character', lazy='dynamic')

	def __init__(self, name, safename):
		self.name = name
		self.safename = safename

	def __repr__(self):
		return '<Character %r>' % (self.name.encode('utf8'))

class Move(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	char_id = db.Column(db.Integer, db.ForeignKey('character.id'))
	name = db.Column(db.String(255))
	damage = db.Column(db.String(255))
	hitstun = db.Column(db.String(255))
	blockstun = db.Column(db.String(255))
	knockback = db.Column(db.String(255))
	angle = db.Column(db.String(255))
	startup = db.Column(db.String(255))
	active = db.Column(db.String(255))
	recovery = db.Column(db.String(255))
	landing = db.Column(db.String(255))
	auto = db.Column(db.String(255))
	iasa = db.Column(db.String(255))
	onblock = db.Column(db.String(255))
	onhit = db.Column(db.String(255))
	notes = db.Column(db.String(2555))
	gifname = db.Column(db.String(255))

	def __init__(self, char_id, name, damage, hitstun, blockstun, knockback, angle, startup, active, recovery, iasa, onblock):
		self.char_id = char_id
		self.name = name
		self.damage = damage
		self.hitstun = hitstun
		self.blockstun = blockstun
		self.knockback = knockback
		self.angle = angle
		self.startup = startup
		self.active = active
		self.recovery = recovery
		self.iasa = iasa
		self.onblock = onblock

	def __repr__(self):
		return '<Move %r:%r>' % (self.char_id, self.name)


class Smashup(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	char = db.Column(db.String(25))
	oppo = db.Column(db.String(25)) 
	suggs = db.relationship('Suggestion', backref='smashup', lazy='dynamic')

	def __init__(self, char, oppo):
		self.char = char
		self.oppo = oppo

	def __repr__(self):
		return '<Smashup %r vs %r>' % (self.char, self.oppo)

class Suggestion(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	section = db.Column(db.String(42))
	char_id = db.Column(db.Integer, db.ForeignKey('character.id'))
	smash_id = db.Column(db.Integer, db.ForeignKey('smashup.id'))
	text = db.Column(db.Text)
	user_nickname = db.Column(db.Integer, db.ForeignKey('user.nickname'))
	voters = db.relationship('User', secondary=votes, lazy='dynamic')
	is_special = db.Column(db.Boolean)
	score = db.Column(db.Integer)

	def __init__(self, section, text, user_nickname):
		self.section = section
		self.text = text
		self.user_nickname = user_nickname
		self.score = 1

	def __repr__(self):
		return '<Suggestion %r: %r, %r, %r>' % (self.id, self.user_nickname, self.section, self.text[0:15])

class DevTip(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text)
	user_name = db.Column(db.Integer, db.ForeignKey('user.nickname'))

	def __init__(self, text):
		self.text = text

	def __repr__(self):
		return '<Suggestion %r: %r>' % (self.id,self.text[0:15])

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True, unique=True)
	nickname = db.Column(db.String(42))
	email = db.Column(db.String(255))
	password = db.Column(db.String(255))
	pw_hash = db.Column(db.String(255))
	about = db.Column(db.Text())
	main = db.Column(db.String(25))
	suggestions = db.relationship('Suggestion', backref='author', lazy='dynamic')
	votes = db.relationship('Suggestion', secondary=votes, lazy='dynamic') 
	is_special = db.Column(db.Boolean)
	powerlevel = db.Column(db.Integer)
	
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


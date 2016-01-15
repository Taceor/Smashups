from __future__ import print_function
import sys
import random
from app import app, db, models, lm
from app.models import Character, Smashup, User, Suggestion, DevTip
from app.forms import LoginForm, NewUser, EditUser, SmashSuggestionForm, CharSuggestionForm, DevSuggestionForm
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_required, login_user, logout_user, current_user
from config import SECRET_KEY

chars = ["Bowser", "Captain Falcon", "Charizard", "Diddy Kong", "Donkey Kong", "Falco", "Fox", "Mr. Game & Watch", "Ganondorf", "Ice Climbers", "Ike", "Ivysaur", "Jigglypuff", "King Dedede", "Kirby", "Link", "Lucario", "Lucas", "Luigi", "Mario", "Marth", "Meta Knight", "Mewtwo", "Ness", "Olimar", "Peach", "Pikachu", "Pit", "R.O.B.", "Roy", "Samus", "Sheik", "Snake", "Sonic", "Squirtle", "Toon Link", "Wario", "Wolf", "Yoshi", "Zelda", "Zero Suit Samus"]

@app.before_request
def before_request():
	g.user = current_user

@app.route('/_upvote')
def upvote():
	user_nickname = request.args.get('user_nickname', 0)
	user = User.query.filter_by(nickname=user_nickname).first()
	sugg_id = request.args.get('sugg_id', 0, type=int)
	sugg = Suggestion.query.filter_by(id=sugg_id).first()
	sugg.score += 1
	sugg.voters.append(user)
	user.votes.append(sugg)
	db.session.add(sugg)
	db.session.add(user)
	db.session.commit()
	return jsonify(result="test")


@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html') 

@app.route('/character/<name>')
def character(name=None):
	if name == 'Random' or name == 'random':
		name = Character.query.filter_by(id=random.randint(1,41)).first().name
	character = Character.query.filter_by(name=name.lower()).first()
	quicks = character.suggs.filter_by(section='quick').join(Character.suggs).order_by(Suggestion.score).all()
	depths = character.suggs.filter_by(section='depth').all()
	return render_template('character.html', character=character, quicks=quicks, depths=depths)

@app.route('/smashup/<char>/<oppo>')
def smashup(char=None, oppo=None):
	if char == 'Random' or char == 'random':
		char = Character.query.filter_by(id=random.randint(1,41)).first().name
	if oppo == 'Random' or oppo == 'random':
		oppo = Character.query.filter_by(id=random.randint(1,41)).first().name
	left = Smashup.query.filter_by(char=char.lower(), oppo=oppo.lower()).first()
	l_pros = left.suggs.filter_by(section='pro').order_by(score.desc()).all()
	l_cons = left.suggs.filter_by(section='con').all()
	l_neuts = left.suggs.filter_by(section='neutral').all()
	right = Smashup.query.filter_by(char=oppo.lower(), oppo=char.lower()).first()
	r_pros = right.suggs.filter_by(section='pro').all()
	r_cons = right.suggs.filter_by(section='con').all()
	r_neuts = right.suggs.filter_by(section='neutral').all()

	return render_template('smashup.html', left=left, right=right, l_pros=l_pros, l_cons=l_cons, l_neuts=l_neuts, r_pros=r_pros, r_cons=r_cons, r_neuts=r_neuts)

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(nickname=form.nickname.data).first()
		if user.check_password(form.password.data):
			login_user(user)
			flash('Logged in user: %r' % user.nickname)
			return redirect(url_for('index'))
		else:
			flash('Bad password, scrub.')
			return redirect(url_for('login'))
	return render_template('login.html', title="Log In", form=form)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
	form = EditUser()
	user = g.user
	if form.validate_on_submit():
		user.about = form.about.data
		user.main = form.main.data
		db.session.add(user)
		db.session.commit()
		flash('Saved About')
		return redirect(url_for('index'))
	else:
		form.about.data = g.user.about
		form.main.data = g.user.main
	return render_template('edituser.html', title="Settings", form=form) 

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect( url_for('index'))

@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
	form = NewUser()
	if form.validate_on_submit():
		user = User(form.nickname.data, form.email.data, form.password.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		flash('Logged in')
		return redirect(url_for('index'))
	return render_template('newuser.html', form=form)

@app.route('/suggestion/<subject>', methods=['GET', 'POST'])
@login_required
def suggestion(subject=None):
	if subject == 'smashup':
		form = SmashSuggestionForm()
		if form.validate_on_submit():
			char = Character.query.filter_by(name=form.character.data.lower()).first()
			oppo = Character.query.filter_by(name=form.opponent.data.lower()).first()
			smashup = Smashup.query.filter_by(char=char.name, oppo=oppo.name).first()
			if form.section.data in ['pro', 'con', 'neutral']:
				sugg = Suggestion(form.section.data, form.text.data, g.user.nickname)
				sugg.smash_id = smashup.id
				if g.user.is_special:
					sugg.is_special = True
				db.session.add(sugg)
				db.session.commit()
				return redirect(url_for('smashup', char=char.name, oppo=oppo.name))
			else:
				flash('Invalid input detected, pleb!')
				return redirect(url_for('index'))
		return render_template('smashsuggestion.html', form=form, chars=chars)
	elif subject == 'character':
		form = CharSuggestionForm()
		if form.validate_on_submit():
			char = Character.query.filter_by(name=form.character.data.lower()).first()
			if form.section.data in ['quick', 'depth']:
				sugg = Suggestion(form.section.data, form.text.data, g.user.nickname)
				sugg.char_id = char.id
				if g.user.is_special:
					sugg.is_special = True
				db.session.add(sugg)
				db.session.commit()
				return redirect(url_for('character', name=char.name))
			else:
				flash('Invalid input detected, pleb!')
				return redirect(url_for('index'))
		return render_template('charsuggestion.html', form=form, chars=chars)
	elif subject == 'developer':
		form = DevSuggestionForm()
		if form.validate_on_submit():
			devtip = DevTip(form.text.data)
			db.session.add(devtip)
			db.session.commit()
			flash('Thanks for your input!')
			return redirect(url_for('index'))
		return render_template('devsuggestion.html', form=form)
	else:
		flash ('Error, no such page')
		return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user == None:
		flash('User not found: %s' % nickname)
		return redirect(url_for('index'))
	return render_template('user.html', user=user, title=user.nickname)

""" def find
	form = FindForm()
	return find.thing.data
"""

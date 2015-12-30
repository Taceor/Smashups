import random
from app import app, db, models, lm
from app.models import Character, Smashup, Pro, Con, Neutral, User, Suggestion, Quick, Depth
from app.forms import LoginForm, NewUser, EditUser, SuggestionForm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required, login_user, logout_user, current_user
from config import SECRET_KEY

@app.before_request
def before_request():
	g.user = current_user

@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html') 

@app.route('/character/<name>')
def character(name=None):
	if name == 'Random':
		name = Character.query.filter_by(id=random.randint(1,41)).first().name
	character = Character.query.filter_by(name=name.lower()).first()
	return render_template('character.html', character=character)

@app.route('/smashup/<char>/<oppo>')
def smashup(char=None, oppo=None):
	left = Smashup.query.filter_by(char=char.lower(), oppo=oppo.lower()).first()
	right = Smashup.query.filter_by(char=oppo.lower(), oppo=char.lower()).first()

	return render_template('smashup.html', left=left, right=right)

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

@app.route('/suggestion', methods=['GET', 'POST'])
def suggestion():
	form = SuggestionForm()
	if form.validate_on_submit():
		char = Character.query.filter_by(name=form.character.data).first()
		if form.opponent.data == 'none':
			if form.section.data == 'quick':
				quick = Quick(form.text.data, char.id)
				db.session.add(quick)
				db.session.commit()
			elif form.section.data == 'depth':
				depth = Depth(form.text.data, char.id)
				db.session.add(depth)
				db.session.commit()
			else:
				flash('Invalid input detected, pleb!')
				return redirect(url_for('suggestion'))
		else:
			oppo = Character.query.filter_by(name=form.opponent.data).first()
			smashup = Smashup.query.filter_by(char=char.name, oppo=oppo.name).first()
			if form.section.data == 'pro':
				pro = Pro(form.text.data, smashup.id)
				db.session.add(pro)
				db.session.commit()
			elif form.section.data == 'con':
				con = Con(form.text.data, smashup.id)
				db.session.add(con)
				db.session.commit()
			elif form.section.data == 'neutral':
				neut = Neut(form.text.data, smashup.id)
				db.session.add(neut)
				db.session.commit()
			else:
				flash('Invalid input detected, pleb!')
				return redirect(url_for('suggestion'))
		return redirect(url_for('character', name=char.name))
	return render_template('suggestion.html', form=form)

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

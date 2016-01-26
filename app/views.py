from __future__ import print_function
import sys
import random, markdown
from app import app, db, models, lm
from app.models import Character, Smashup, User, Suggestion, DevTip
from app.forms import LoginForm, NewUser, EditUser, SmashSuggestionForm, CharSuggestionForm, DevSuggestionForm
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, Markup
from flask.ext.login import login_required, login_user, logout_user, current_user
from config import SECRET_KEY

chars = ["Bowser", "Captain Falcon", "Charizard", "Diddy Kong", "Donkey Kong", "Falco", "Fox", "Mr. Game & Watch", "Ganondorf", "Ice Climbers", "Ike", "Ivysaur", "Jigglypuff", "King Dedede", "Kirby", "Link", "Lucario", "Lucas", "Luigi", "Mario", "Marth", "Meta Knight", "Mewtwo", "Ness", "Olimar", "Peach", "Pikachu", "Pit", "R.O.B.", "Roy", "Samus", "Sheik", "Snake", "Sonic", "Squirtle", "Toon Link", "Wario", "Wolf", "Yoshi", "Zelda", "Zero Suit Samus"]

@app.before_request
def before_request():
	g.user = current_user

@app.template_filter('markdown')
def markdown_filter(data):
    from flask import Markup
    from markdown import markdown
    return Markup(markdown(data))

@app.route('/_upvote', methods=['GET', 'POST'])
def upvote():
	user_nickname = request.form.get('user_nickname')
	user = User.query.filter_by(nickname=user_nickname).first()
	sugg_id = request.form.get('sugg_id')
	sugg = Suggestion.query.filter_by(id=sugg_id).first()
	if sugg.voters.filter_by(nickname=user_nickname).first() is not None:
		print("ERR", file=sys.stderr)
		print("Sugg_id: %r" % (sugg_id), file=sys.stderr)
		print("Sugg.id: %r" % (sugg.id), file=sys.stderr)
		print("User: %r" % (user), file=sys.stderr)
		print(sugg.voters.all(), file=sys.stderr)
	else:
		print("VOTED", file=sys.stderr)
		sugg.score += 1
		sugg.voters.append(user)
		db.session.add(sugg)
		db.session.commit()
	return jsonify(result="test")

@app.route('/_delete_suggestion', methods=['GET', 'POST'])
def delete_suggestion():
	user_nickname = request.form.get('user_nickname')
	user = User.query.filter_by(nickname=user_nickname).first()
	sugg_id = request.form.get('sugg_id')
	sugg = Suggestion.query.filter_by(id=sugg_id).first()
	if user.is_special or (user.nickname == sugg.user_nickname):
		for u in sugg.voters.all():
			sugg.voters.remove(u)
			db.session.commit()
		db.session.delete(sugg)
		db.session.commit()
	else:
		flash('You are not cool enough to do that!')
		return redirect(url_for('index'))
	return jsonify(result="test")


@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html') 

@app.route('/character/<name>')
@app.route('/character/<name>/<section>')
def character(name=None, section=None):
	if name == 'Random' or name == 'random':
		name = Character.query.filter_by(id=random.randint(1,41)).first().name
	character = Character.query.filter_by(name=name.lower()).first()
	if section == 'quicktips':
		quicks = character.suggs.filter_by(section='quick').join(Character.suggs).order_by(Suggestion.score.desc()).all()
		return render_template('quicktips.html', character=character, quicks=quicks)
	elif section == 'indepth':
		depths = character.suggs.filter_by(section='depth').join(Character.suggs).order_by(Suggestion.score.desc()).all()
		return render_template('indepth.html', character=character, depths=depths)
	else:
		quicks = character.suggs.filter_by(section='quick').join(Character.suggs).order_by(Suggestion.score.desc()).limit(10).all()
		depths = character.suggs.filter_by(section='depth').join(Character.suggs).order_by(Suggestion.score.desc()).limit(10).all()
		return render_template('character.html', character=character, quicks=quicks, depths=depths)

@app.route('/smashup/<char>/<oppo>')
def smashup(char=None, oppo=None):
	if char == 'Random' or char == 'random':
		char = Character.query.filter_by(id=random.randint(1,41)).first().name
	if oppo == 'Random' or oppo == 'random':
		oppo = Character.query.filter_by(id=random.randint(1,41)).first().name
	left = Smashup.query.filter_by(char=char.lower(), oppo=oppo.lower()).first()
	l_pros = left.suggs.filter_by(section='pro').join(Smashup.suggs).order_by(Suggestion.score.desc()).limit(5).all()
	l_cons = left.suggs.filter_by(section='con').join(Smashup.suggs).order_by(Suggestion.score.desc()).limit(5).all()
	l_neuts = left.suggs.filter_by(section='neutral').join(Smashup.suggs).order_by(Suggestion.score.desc()).limit(5).all()
	right = Smashup.query.filter_by(char=oppo.lower(), oppo=char.lower()).first()
	r_pros = right.suggs.filter_by(section='pro').join(Smashup.suggs).order_by(Suggestion.score.desc()).limit(5).all()
	r_cons = right.suggs.filter_by(section='con').join(Smashup.suggs).order_by(Suggestion.score.desc()).limit(5).all()
	r_neuts = right.suggs.filter_by(section='neutral').join(Smashup.suggs).order_by(Suggestion.score.desc()).limit(5).all()

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

@app.route('/test/<list:chars>/<list:oppos>')
def test(chars, oppos):
	string = ""
	string2 = ""
	for char in chars:
		string += char + " "
	for oppo in oppos:
		string2 += oppo + " "
	return string + string2


@app.route('/suggestion/<subject>', methods=['GET', 'POST'])
@app.route('/suggestion/<subject>/<section>/<list:characters>', methods=['GET', 'POST'])
@app.route('/suggestion/<subject>/<section>/<list:characters>/<list:opponents>', methods=['GET', 'POST'])
@login_required
def suggestion(subject=None, characters=None, opponents=None, section=None):
	if subject == 'smashup':
		form = SmashSuggestionForm(section=section)
		form.characters.data = characters
		form.opponents.data = opponents
		if form.validate_on_submit():
			for char in form.characters.data:
				char = Character.query.filter_by(name=char.lower()).first()
				for oppo in form.opponents.data:
					oppo = Character.query.filter_by(name=oppo.lower()).first()
					smashup = Smashup.query.filter_by(char=char.name, oppo=oppo.name).first()
					sugg = Suggestion(form.section.data, form.text.data, g.user.nickname)
					sugg.smash_id = smashup.id
					if g.user.is_special:
						sugg.is_special = True
					db.session.add(sugg)
					db.session.commit()
			return redirect(url_for('smashup', char=char.name, oppo=oppo.name))
		return render_template('smashsuggestion.html', form=form)
	elif subject == 'character':
		form = CharSuggestionForm(section=section)
		form.characters.data = characters
		if form.validate_on_submit():
			for char in form.characters.data:
				char = Character.query.filter_by(name=char.lower()).first()
				sugg = Suggestion(form.section.data, form.text.data, g.user.nickname)
				sugg.char_id = char.id
				if g.user.is_special:
					sugg.is_special = True
				db.session.add(sugg)
				db.session.commit()
			return redirect(url_for('character', name=char.name))
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

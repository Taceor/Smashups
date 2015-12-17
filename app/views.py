import random
from app import app, db, models
from app.models import Character, Smashup, Pro, Con, Neutral
from flask import render_template, flash, redirect, session, url_for, request

@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html') 

@app.route("/yoshi")
def yoshi():
	return render_template('yoshi.html')

@app.route('/character/<name>')
def character(name=None):
	if name == 'Random':
		name = Character.query.filter_by(id=random.randint(1,41)).first().name
	character = Character.query.filter_by(name=name.lower()).first()
	return render_template('character.html', character=character)

@app.route('/smashup')
def smashup():
	return render_template('smashup.html')

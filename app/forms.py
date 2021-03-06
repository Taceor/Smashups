from flask.ext.wtf import Form
from wtforms.fields import StringField, BooleanField, TextAreaField, PasswordField, TextField, SelectField, SelectMultipleField
from wtforms import validators

characters = [("bowser", "Bowser"), ("captain falcon", "Captain Falcon"), ("charizard", "Charizard"), ("diddy kong", "Diddy Kong"), ("donkey kong", "Donkey Kong"), ("falco", "Falco"), ("fox", "Fox"), ("mr. game & watch", "Mr. Game & Watch"), ("ganondorf", "Ganondorf"), ("ice climbers", "Ice Climbers"), ("ike", "Ike"), ("ivysaur", "Ivysaur"), ("jigglypuff", "Jigglypuff"), ("king dedede", "King Dedede"), ("kirby", "Kirby"), ("link", "Link"), ("lucario", "Lucario"), ("lucas", "Lucas"), ("luigi", "Luigi"), ("mario", "Mario"), ("marth", "Marth"), ("meta knight", "Meta Knight"), ("mewtwo", "Mewtwo"), ("ness", "Ness"), ("olimar", "Olimar"), ("peach", "Peach"), ("pikachu", "Pikachu"), ("pit", "Pit"), ("r.o.b.", "R.O.B."), ("roy", "Roy"), ("samus", "Samus"), ("sheik", "Sheik"), ("snake", "Snake"), ("sonic", "Sonic"), ("squirtle", "Squirtle"), ("toon link", "Toon Link"), ("wario", "Wario"), ("wolf", "Wolf"), ("yoshi", "Yoshi"), ("zelda", "Zelda"), ("zero suit samus", "Zero Suit Samus")]
characters2 = [("bowser", "Bowser"), ("captain falcon", "Captain Falcon"), ("charizard", "Charizard"), ("diddy kong", "Diddy Kong"), ("donkey kong", "Donkey Kong"), ("falco", "Falco"), ("fox", "Fox"), ("mr. game & watch", "Mr. Game & Watch"), ("ganondorf", "Ganondorf"), ("ice climbers", "Ice Climbers"), ("ike", "Ike"), ("ivysaur", "Ivysaur"), ("jigglypuff", "Jigglypuff"), ("king dedede", "King Dedede"), ("kirby", "Kirby"), ("link", "Link"), ("lucario", "Lucario"), ("lucas", "Lucas"), ("luigi", "Luigi"), ("mario", "Mario"), ("marth", "Marth"), ("meta knight", "Meta Knight"), ("mewtwo", "Mewtwo"), ("ness", "Ness"), ("olimar", "Olimar"), ("peach", "Peach"), ("pikachu", "Pikachu"), ("pit", "Pit"), ("r.o.b.", "R.O.B."), ("roy", "Roy"), ("samus", "Samus"), ("sheik", "Sheik"), ("snake", "Snake"), ("sonic", "Sonic"), ("squirtle", "Squirtle"), ("toon link", "Toon Link"), ("wario", "Wario"), ("wolf", "Wolf"), ("yoshi", "Yoshi"), ("zelda", "Zelda"), ("zero suit samus", "Zero Suit Samus")]

class LoginForm(Form):
	nickname = TextField('Nickname', [validators.DataRequired()])
	password = StringField('Password', [validators.DataRequired()])

class NewUser(Form):
	nickname = StringField('Nickname', [validators.DataRequired()])
	email = StringField('email', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')

class EditUser(Form):
	about = TextAreaField('About You', [validators.DataRequired()])
	main = SelectField('Select Main', choices=[('yoshi', 'Yoshi'), ('not', 'Not')])

class CharSuggestionForm(Form):
	characters = SelectMultipleField(u'Select Characters', choices=characters)
	section = SelectField(u'Select Section', choices=[('quick', 'Quick Tip'), ('depth', 'In-Depth')])
	text = TextAreaField(u'Suggestion')

class SmashSuggestionForm(Form):
	characters = SelectMultipleField('Select Characters', choices=characters)
	opponents = SelectMultipleField('Select Opponents', choices=characters2)
	section = SelectField(u'Select Section', choices=[('pro', 'Pro'), ('con', 'Con'), ('neutral', 'Neutral')])
	text = TextAreaField(u'Suggestion')

class DevSuggestionForm(Form):
	text = TextAreaField('Suggestion')

class CommentForm(Form):
    comment_text = TextAreaField('Comment')

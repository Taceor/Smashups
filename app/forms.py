from flask.ext.wtf import Form
from wtforms.fields import StringField, BooleanField, TextAreaField, PasswordField, TextField, SelectField
from wtforms import validators

class LoginForm(Form):
	nickname = TextField('Nickname', [validators.DataRequired()])
	password = StringField('Password', [validators.DataRequired()])

class NewUser(Form):
	nickname = StringField('Nickname', [validators.DataRequired()])
	email = StringField('email', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')

class EditUser(Form):
	about = TextField('About You', [validators.DataRequired()])
	main = SelectField('Select Main', choices=[('yoshi', 'Yoshi'), ('not', 'Not')])

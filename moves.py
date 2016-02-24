#!flask/bin/python
import app
from app import models, db
from app.models import Character, Move
import json

with open('FrameData_AllCharacters.json') as data_file:
	data = json.load(data_file)

for action in data['Bowser']['SubActions']:
	if data['Bowser']['SubActions'][action]['Hitboxes']:
		damage = data['Bowser']['SubActions'][action]['DetailedHitboxData'][0]['collisions'][0]['Damage']
		hitboxes  = data['Bowser']['SubActions'][action]['Hitboxes']
		print action
		print damage
		print hitboxes

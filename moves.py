#!flask/bin/python
import app
from app import models, db
from app.models import Character, Move
import json

chars = ["Bowser", "Captain Falcon", "Charizard", "Diddy Kong", "Donkey Kong", "Falco", "Fox", "Mr. Game & Watch", "Ganondorf", "Ice Climbers", "Ike", "Ivysaur", "Jigglypuff", "King Dedede", "Kirby", "Link", "Lucario", "Lucas", "Luigi", "Mario", "Marth", "Meta Knight", "Ness", "Olimar", "Peach", "Pikachu", "Pit", "R.O.B", "Roy", "Samus", "Sheik", "Snake", "Sonic", "Squirtle", "Toon Link", "Wario", "Wolf", "Yoshi", "Zelda"]

#load data
with open('FrameData_AllCharacters.json') as data_file:
    data = json.load(data_file)

top = 0

#Parse data for important move info
for character in chars:
    for action in data[character]['SubActions']:
        damage = []
        dam = []
        try:
            hitbox_frames  = data[character]['SubActions'][action]['Hitboxes']
            for hitbox in range(len(hitbox_frames)):
                dam=[]
                for damage_value in range(len(data[character]['SubActions'][action]['DetailedHitboxData'][hitbox]['collisions'])):
                    d = data[character]['SubActions'][action]['DetailedHitboxData'][hitbox]['collisions'][damage_value]['Damage']
                    dam.append(d)
                damage.append(dam)

            print "\nAction: %s" % action
            print "Hitbox Frames: %s" % hitbox_frames
            print "Damage: %s" % damage
        except e:
            print "Char %s: %s" % character, e
            #print "Char:%s, Action:%s, Frames:%s, Dmg:%s" % character, action, hitbox_frames, damage

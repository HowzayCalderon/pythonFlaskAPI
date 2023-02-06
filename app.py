from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('anime', user='postgres', password='12345', host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = db 

class Show(BaseModel):
    name = CharField()
    anime_type = CharField()

class Character(BaseModel):
    name = CharField()
    main_character = BooleanField()
    show_id = IntegerField()

db.connect()
db.drop_tables([Character])
db.drop_tables([Show])
db.create_tables([Show])
db.create_tables([Character])

# Show(name= 'Naruto', main_character= 'Naruto Uzumaki', anime_type= 'Shonen').save()
# Show(name= 'Attack On Titan', main_character= 'Eren Yeager', anime_type= 'Shonen').save()

show_data = [
    {"name": 'Dragonball Z',"anime_type": 'Shonen'},
    {"name": 'YuGhi-Oh', "anime_type": 'Shonen'},
    {"name": 'Demon Slayer', "anime_type": 'Shonen'},
    {"name": 'Rurouni Kenshin', "anime_type": 'Shonen'},
    {"name": 'Naruto', "anime_type": 'Shonen'},
    {"name": 'Attack On Titan', "anime_type": "Shonen"},
    {"name": "FullMetal Alchemist", "anime_type": 'Shonen'},
    {"name": 'Hellsing Ultimate', "anime_type": 'Seinen'},
    {"name": 'Tokyo Ghoul', "anime_type": 'Seinen'},
    {"name": 'One Punch Man', "anime_type": 'Seinen'},
    {"name": 'Initial D First Stage', "anime_type": 'Seinen'},
    {"name": 'Black Clover', "anime_type": 'Shonen'},
    {"name": 'Jujutsu Kaisen', "anime_type": 'Shonen'},
    {"name": 'One Piece', "anime_type": 'Shonen'},
    {"name": 'Spy x Family', "anime_type": 'Shonen'},
    {"name": 'Hunter x Hunter', "anime_type": 'Shonen'},
    {"name": 'Bleach', "anime_type": 'Shonen'},
    {"name": 'Fire Force', "anime_type": 'Shonen'},
    {"name": 'YuYu Hakusho', "anime_type": 'Shonen'},
    {"name": 'Death Note', "anime_type": 'Shonen'},
    {"name": 'Chainsaw Man', "anime_type": 'Shonen'},
    {"name": 'InuYasha', "anime_type": 'Shonen'},
    {"name": 'Trigun', "anime_type": 'Shonen'},
    {"name": 'Mobile Fighter G Gundam', "anime_type": 'Shonen'}


]

character_data = [
    {"name": 'Monkey D. Luffy', "main_character": "True", "show_id": 14}
]

Show.insert_many(show_data).execute()
Character.insert_many(character_data).execute()

app = Flask(__name__)

@app.route('/show/', methods=['GET', 'POST'])
@app.route('/show/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Show.get(Show.id == id)))
        else:
            show_list = []
            for show in Show.select():
                show_list.append(model_to_dict(show))
            return jsonify(show_list)
    elif request.method == 'PUT':
        body = request.get_json()
        Show.update(body).where(Show.id == id).execute()
        return "Show" + str(id) + "has been updated."
    
    elif request.method == 'POST':
        new_show = dict_to_model(Show, request.get_json())
        new_show.save()
        return jsonify({"success": True})

    elif request.method == 'DELETE':
        Show.delete().where(Show.id == id).execute()
        return "Show" + str(id) + "deleted."

@app.route('/character/', methods=['GET', 'POST'])
@app.route('/character/<id>', methods=['GET', 'PUT', 'DELETE'])
def cendpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Character.get(Character.id == id)))
        else:
            character_list = []
            for character in Character.select():
                character_list.append(model_to_dict(character))
            return jsonify(character_list)

    elif request.method == 'PUT':
        body = request.get_json()
        Character.update(body).where(Character.id == id).execute()
        return "Character" + str(id) + "has been updated."

    elif request.method == 'DELETE':
        Character.delete().where(Character.id == id).execute()
        return "Character" + str(id) + "deleted."

    elif request.method == 'POST':
        new_character = dict_to_model(Character, request.get_json())
        new_character.save()
        return jsonify({"success": True})


    
app.run(debug=True, port=3000)
   

# shonen: anime for young boys, shoujo: anime for young girls, seinen: anime for young adult males (18+), josei: anime for young adult females (18+), kodomomuke: anime for young children (4-12?)
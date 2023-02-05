from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('anime', user='postgres', password='12345', host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = db 

class Show(BaseModel):
    name = CharField()
    main_character = CharField()
    anime_type = CharField()

db.connect()
db.drop_tables([Show])
db.create_tables([Show])

# Show(name= 'Naruto', main_character= 'Naruto Uzumaki', anime_type= 'Shonen').save()
# Show(name= 'Attack On Titan', main_character= 'Eren Yeager', anime_type= 'Shonen').save()

data = [
    {"name": 'Dragonball Z', "main_character": 'Goku', "anime_type": 'Shonen'},
    {"name": 'YuGhi-Oh', "main_character": 'Yugi', "anime_type": 'Shonen'},
    {"name": 'Demon Slayer', "main_character": 'Tanjiro', "anime_type": 'Shonen'},
    {"name": 'Rurouni Kenshin', "main_character": 'Kenshin Himura', "anime_type": 'Shonen'},
    {"name": 'Naruto', "main_character": 'Naruto Uzumaki', "anime_type": 'Shonen'},
    {"name": 'Attack On Titan', "main_character": 'Eren Yeager', "anime_type": "Shonen"},
    {"name": "FullMetal Alchemist", "main_character": "Edward Elric", "anime_type": 'Shonen'},
    {"name": 'Hellsing Ultimate', "main_character": 'Alucard', "anime_type": 'Seinen'},
    {"name": 'Tokyo Ghoul', "main_character": 'Ken Kaneki', "anime_type": 'Seinen'},
    {"name": 'One Punch Man', "main_character": 'Saitama', "anime_type": 'Seinen'},
    {"name": 'Initial D First Stage', "main_character": 'Takumi Fujiwara', "anime_type": 'Seinen'},
    {"name": 'Black Clover', "main_character": 'Asta', "anime_type": 'Shonen'},
    {"name": 'Jujutsu Kaisen', "main_character": 'Yuji Itadori', "anime_type": 'Shonen'},
    {"name": 'One Piece', "main_character": "Monkey D. Luffy", "anime_type": 'Shonen'},
    {"name": 'Spy x Family', "main_character": 'Loid Forger (Twilight)', "anime_type": 'Shonen'},
    {"name": 'Hunter x Hunter', "main_character": 'Gon Freecss', "anime_type": 'Shonen'},
    {"name": 'Bleach', "main_character": 'Ichigo Kurosaki', "anime_type": 'Shonen'},
    {"name": 'Fire Force', "main_character": 'Maki Oze', "anime_type": 'Shonen'},
    {"name": 'YuYu Hakusho', "main_character": 'Yusuke Urameshi', "anime_type": 'Shonen'}

]

Show.insert_many(data).execute()

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
    if request.method == 'PUT':
        body = request.get_json()
        Show.update(body).where(Show.id == id).execute()
        return "Show" + str(id) + "has been updated."
    
    if request.method == 'POST':
        new_show = dict_to_model(Show, request.get_json())
        new_show.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        Show.delete().where(Show.id == id).execute()
        return "Show" + str(id) + "deleted."

app.run(debug=True)
   

# shonen: anime for young boys, shoujo: anime for young girls, seinen: anime for young adult males (18+), josei: anime for young adult females (18+), kodomomuke: anime for young children (4-12?)
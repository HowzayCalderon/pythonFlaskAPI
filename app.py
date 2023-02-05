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

Show(name= 'Naruto', main_character= 'Naruto Uzumaki', anime_type= 'Shonen').save()

Show

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

app.run()
   

# shonen: anime for young boys, shoujo: anime for young girls, seinen: anime for young adult males (18+), josei: anime for young adult females (18+), kodomomuke: anime for young children (4-12?)
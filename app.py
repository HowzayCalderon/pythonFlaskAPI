from flask import Flask, jsonify, request
from peewee import *

db = PostgresqlDatabase('anime', user='postgres', password='12345', host='localhost', port=3000)

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


   

# shonen: anime for young boys, shoujo: anime for young girls, seinen: anime for young adult males (18+), josei: anime for young adult females (18+), kodomomuke: anime for young children (4-12?)
from flask import Flask, jsonify, request
from peewee import *

db = PostgresqlDatabase()
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('game.sqlite')

class User(UserMixin, Model):
  username = CharField()
  email = CharField()
  password = CharField()

  class Meta: 
    database = DATABASE

class Review(Model):
    game_id = CharField()
    user_id = ForeignKeyField(User)
    title = CharField() 
    up_votes = CharField() 
    down_votes = CharField() 
    body = CharField()
    is_positive = BooleanField()
    class Meta: database = DATABASE


def initialize():
  DATABASE.connect()
  DATABASE.create_tables([User, Review], safe=True)
  print("Tables Created")
  DATABASE.close()
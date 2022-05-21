import datetime
import time
from datetime import *
from time import *
from peewee import *

db = MySQLDatabase(user='root', password='root',database='tele', host='127.0.0.1')

class BaseClass(Model):
    class Meta:
        database = db

class City(BaseClass):
    name = CharField()

    def get_list(self):
        list = []
        for x in self.select():
            list.append(x)
        return list



class Person(BaseClass):
    user_id = CharField()
    city = ForeignKeyField(City, backref='cities')
    join_date = DateField(default=datetime.now())
    status = CharField(default=1)


class Ad(BaseClass):
    owner = ForeignKeyField(Person, backref='owners')
    city = ForeignKeyField(City, backref='cities')
    title = CharField()
    description = CharField()
    photo = CharField()
    price = DecimalField(max_digits=10, decimal_places=2, auto_round=False)
    create_date = DateField(default=datetime.now())
    status = CharField(default=1)

class Category(BaseClass):
    category = CharField(default='default')


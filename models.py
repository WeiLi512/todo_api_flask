from peewee import *

DATABASE = SqliteDatabase('todos.sqlite')


class Todo(Model):
    """Todo Model"""
    id = AutoField()
    name = CharField(null=False)
    completed = BooleanField(default=False)

    class Meta:
        database = DATABASE


def initialize():
    """Initialize db and create tables"""
    DATABASE.connect(reuse_if_open=True)
    DATABASE.create_tables([Todo], safe=True)
    DATABASE.close()

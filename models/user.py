from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField(unique=True)
    full_name = fields.CharField(max_length=80, null=True)
    username = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = "users"

# class UserData(Model):
#     id = fields.IntField(pk=True)
#     user_id = fields.BigIntField(unique=True)
#     full_name = fields.CharField(max_length=80, null=True)
#     username = fields.CharField(max_length=50, unique=True)
#     voice = fields.CharField(max_length=50)
#     language = fields.CharField(max_length=30)
#
#     class Meta:
#         table = "user_data"
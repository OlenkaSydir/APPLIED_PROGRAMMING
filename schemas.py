from models import User
from marshmallow import Schema, fields


class UserSchema(Schema):
    class Meta:
        model = User
        fields = ('id', 'user_name', 'email')

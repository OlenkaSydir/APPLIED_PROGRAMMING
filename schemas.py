from models import User, Note
from marshmallow import Schema, fields


class UserSchema(Schema):
    class Meta:
        model = User
        fields = ('id', 'user_name', 'email')

class NoteSchema(Schema):
    class Meta:
        model = Note
        fields = ('id', 'note_text', 'owner_id', 'tag_id')

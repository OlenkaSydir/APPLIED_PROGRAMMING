from models import User, Note, ForeignEditor
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class UserSchema(Schema):
    class Meta:
        model = User
        fields = ('id', 'user_name', 'email')

class NoteSchema(Schema):
    class Meta:
        model = Note
        fields = ('id', 'note_text', 'owner_id', 'tag_id')

class ForeignEditorSchema(Schema):
    class Meta:
        model = ForeignEditor
        fields = ('id', 'editor_id')

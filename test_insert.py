from datetime import datetime
from models import Session, User, Tag, Note, ForeignEditor, Edit

session = Session()

user = User(user_name="Naruto", password="23423432432", email="konoha@gmail.com")
user2 = User(user_name="Naruto2", password="23423432432", email="konoha@gmail.com")
editor = User(user_name="Sakura", password="23423432432", email="konoha@gmail.com")
tag = Tag(title="anime")
note = Note(note_text="I love anime", owner_id=1, tag_id=1)
edit = Edit(editor_id=2, note_id=1, edit_timestamp=datetime.today())

foreign_editor = ForeignEditor(editor_id=2, note_id=1)

session.add(user)
session.add(user2)
session.add(editor)
session.add(tag)
session.add(note)
session.add(edit)
session.add(foreign_editor)
session.commit()





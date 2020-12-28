from models import Session, User, Tag, ForeignEditor, Edit
from datetime import datetime


session = Session()


def find_by_email(email):
    try:
        user = session.query(User).filter_by(email=email).one()
    except:
        return None
    return user


def update_util(user, data):
    try:
        if data.get('user_name', None):
            user.user_name = data['user_name']
        if data.get('password', None):
            user.password = data['password']

    except:
        return None

    session.commit()

    return user

def check_if_tag_exists(tag_id):
    try:
        tag = session.query(Tag).filter_by(id=int(tag_id)).one()
    except:
        return False

    return True

def check_if_can_edit(note_id, editor_id):

    try:
        foreign_editor = session.query(ForeignEditor).filter_by(note_id=int(note_id))\
            .filter_by(editor_id=int(editor_id))\
            .one()
    except:
        return False

    return True


def process_edit(edit_dto, note):

    try:
        if edit_dto.get('change', None):
            note.note_text = edit_dto['change']
    except:
        return None

    edit = Edit(editor_id=edit_dto['editor_id'], note_id=note.id, edit_timestamp=datetime.today())

    session.add(edit)
    session.commit()

    return note



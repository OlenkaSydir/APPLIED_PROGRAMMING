from models import Session, User, Tag, ForeignEditor, Edit
from datetime import datetime
from slugify import slugify


session = Session()


def find_by_email(email):
    try:
        user = session.query(User).filter_by(email=email).one()
    except:
        return None
    return user


def update_util(user, data): #?????????
    try:
        if data.get('user_name', None):
            user.user_name = data['user_name']
        if data.get('password', None):
            user.password = data['password']

    except:
        return None

    session.commit()

    return user

def create_or_assign_tag(tag_title):

    slugified_title = slugify(tag_title)
    try:
        tag = session.query(Tag).filter_by(title=slugified_title).one()
    except:
        tag = Tag(title=slugified_title)
        session.add(tag)
        session.commit()

    print(tag.id)

    return tag

def check_if_editor(note, editor_id):

    if editor_id == note.owner_id:
        return True

    try:
        foreign_editor = session.query(ForeignEditor).filter_by(note_id=note.id)\
            .filter_by(editor_id=int(editor_id))\
            .one()
    except:
        return False

    return True


def process_edit(edit_dto, note, editor_id):

    try:
        if edit_dto.get('change', None):
            note.note_text = edit_dto['change']
    except:
        return None

    edit = Edit(editor_id=editor_id, note_id=note.id, edit_timestamp=datetime.today())

    session.add(edit)
    session.commit()

    return note
from flask import Flask, request
from models import Session, User, Note, ForeignEditor
import utils
import constants
from constants import USER_PATH, BASE_PATH, NOTE_PATH, EDITOR_PATH
from schemas import UserSchema, NoteSchema, ForeignEditorSchema
from flask import jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask("__name__")
auth = HTTPBasicAuth()

session = Session()

@app.route('/api/v1/hello-world-<int:var>')
def hello_world(var):
    return 'Hello World ' + str(var)


@app.route(BASE_PATH + USER_PATH, methods=['POST'])
def create_user():
    user_request = request.get_json()
    email = user_request['email']

    if utils.find_by_email(email) != None:
        return jsonify(constants.USER_ALREADY_EXISTS), 400

    user = User(**user_request)
    session.add(user)
    session.commit()

    return jsonify(constants.USER_CREATED), 201


@app.route(BASE_PATH + USER_PATH + "/" + "me", methods=['GET'])
@auth.login_required
def get_user_by_id():
    user = auth.current_user()
    try:
        user = session.query(User).filter_by(id=user.id).one()

    except:
        return jsonify(constants.USER_NOT_FOUND), 404

    return jsonify(UserSchema().dump(user)), 200

@app.route(BASE_PATH + USER_PATH, methods=['GET'])
def get_all_users():
    try:
        users = session.query(User).all()
    except:
        users = []

    users_dto = UserSchema(many=True)

    return jsonify(users_dto.dump(users)), 200

@app.route(BASE_PATH + USER_PATH + '/' + 'update_me', methods=['PUT'])
@auth.login_required
def update_user():
    user = auth.current_user()
    update_request = request.get_json()

    try:
        user = session.query(User).filter_by(id=user.id).one()
    except:
        return jsonify(constants.USER_NOT_FOUND), 404

    update_user = utils.update_util(user, update_request)

    if update_user == None:
        return jsonify(constants.SOMETHING_WENT_WRONG), 400

    return jsonify(constants.USER_UPDATED), 200


@app.route(BASE_PATH + USER_PATH + '/' + 'delete_me', methods=['DELETE'])
@auth.login_required
def delete_user():
    user = auth.current_user()
    try:
        user = session.query(User).filter_by(id=user.id).one()
    except:
        return jsonify(constants.USER_NOT_FOUND), 404

    try:
        notes = session.query(Note).filter_by(owner_id=user.id).all()
        editors = []
        for note in notes:
            editors += session.query(ForeignEditor).filter_by(note_id=note.id).all()
    except:
        notes = []
        editors = []

    for editor in editors:
        session.delete(editor)

    for note in notes:
        session.delete(note)

    session.delete(user)
    session.commit()

    return constants.USER_DELETED, 200


@auth.verify_password
def user_auth(username, password):

    try:
        user = session.query(User).filter_by(user_name=username).one()
    except:
        return None

    if user.password == password:
        return user


@app.route(BASE_PATH + NOTE_PATH + "/add_my_note", methods=['POST'])
@auth.login_required
def create_note():
    user = auth.current_user()
    note_request = request.get_json()
    tag_title = note_request['tag_title']
    user.id = note_request['owner_id']

    tag = utils.create_or_assign_tag(tag_title)

    try:
        user = session.query(User).filter_by(id=user.id).one()

    except:
        return jsonify(constants.USER_NOT_FOUND), 404

    note = Note(note_text=note_request['note_text'], owner_id=note_request['owner_id'], tag_id=tag.id)

    session.add(note)
    session.commit()

    return jsonify(constants.NOTE_CREATED), 201

@app.route(BASE_PATH + NOTE_PATH, methods=['GET'])
def get_all_notes():
    try:
        notes = session.query(Note).all()
    except:
        notes = []

    notes_dto = NoteSchema(many=True)

    return jsonify(notes_dto.dump(notes)), 200

@app.route(BASE_PATH + NOTE_PATH + '/' + '<int:note_id>', methods=['PUT'])
@auth.login_required
def edit_note(note_id):
    user = auth.current_user()
    edit_dto = request.get_json()

    try:
        note = session.query(Note).filter_by(id=int(note_id)).one()
    except:
        return jsonify(constants.NOTE_NOT_FOUND), 404

    if not utils.check_if_editor(note, user.id):
        return jsonify(constants.USER_CANNOT_EDIT), 400

    edited_note = utils.process_edit(edit_dto, note, user.id)

    if edited_note == None:
        return jsonify(constants.SOMETHING_WENT_WRONG), 400

    return jsonify(constants.NOTE_EDITED), 200


@app.route(BASE_PATH + NOTE_PATH + '/' + 'users' + '/' + 'my_notes', methods=['GET'])
@auth.login_required
def get_users_notes():
    user = auth.current_user()
    note_list = NoteSchema(many=True)
    try:
        notes = session.query(Note).filter_by(owner_id=user.id).all()
    except:
        notes = []

    return jsonify(note_list.dump(notes)), 200


@app.route(BASE_PATH + NOTE_PATH + '/' + '<int:note_id>', methods=['GET'])
@auth.login_required
def get_note_by_id(note_id):
    user = auth.current_user()
    try:
        note = session.query(Note).filter_by(id=int(note_id)).one()
    except:
        return jsonify(constants.NOTE_NOT_FOUND), 404
    if user.id == note.owner_id:
        return jsonify(NoteSchema().dump(note)), 200
    else:
        return jsonify(constants.NOTE_UNACCESSABLE), 402


@app.route(BASE_PATH + NOTE_PATH + '/' + '<int:note_id>', methods=['DELETE'])
@auth.login_required
def delete_note(note_id):
    user = auth.current_user()
    try:
        note = session.query(Note).filter_by(id=int(note_id)).one()
    except:
        return jsonify(constants.NOTE_NOT_FOUND), 400

    try:
        editors = session.query(ForeignEditor).filter_by(note_id=int(note_id)).all()
    except:
        editors = []

    for editor in editors:
        session.delete(editor)
    if user.id == note.owner_id:
        session.delete(note)
        session.commit()
        return jsonify(constants.NOTE_DELETED), 200
    else:
        return jsonify(constants.NOTE_UNACCESSABLE), 402


@app.route(BASE_PATH + EDITOR_PATH + '/add_foreign_editor', methods=['POST'])
@auth.login_required
def assign_editor():
    user = auth.current_user()
    editor_dto = request.get_json()
    try:
        note = session.query(Note).filter_by(id=int(editor_dto['note_id'])).one()
    except:
        return jsonify(constants.NOTE_NOT_FOUND), 404

    try:
        editor = session.query(User).filter_by(id=int(editor_dto['editor_id'])).one()
    except:
        return jsonify(constants.EDITOR_NOT_FOUND_ASSIGN), 404

    if user.id != note.owner_id:
        return jsonify(constants.NOTE_UNACCESSABLE), 402
    if utils.check_if_editor(note, editor_dto['editor_id']):
        return jsonify(constants.ALREADY_EDITOR), 400


    try:
        foreign_editors = session.query(ForeignEditor).filter_by(note_id=int(editor_dto['note_id'])).all()
    except:
        foreign_editors = []

    if len(foreign_editors) >= 5:
        return jsonify(constants.EDITORS_OVERFLOW), 400

    foreign_editor = ForeignEditor(**editor_dto)

    session.add(foreign_editor)
    session.commit()

    return jsonify(constants.EDITOR_ASSIGNED), 201


@app.route(BASE_PATH + EDITOR_PATH + '/' + '<int:foreign_editor_id>' + '/notes' + '/' + '<int:note_id>', methods=['DELETE'])
@auth.login_required
def delete_editor(foreign_editor_id, note_id):
    user = auth.current_user()
    try:
        note = session.query(Note).filter_by(id=int(note_id)).one()
    except:
        return jsonify(constants.NOTE_NOT_FOUND), 404

    try:
        foreign_editor = session.query(ForeignEditor).filter_by(id=foreign_editor_id).one()

    except:
        return jsonify(constants.EDITOR_NOT_FOUND), 404

    if note.owner_id == user.id:
        session.delete(foreign_editor)
        session.commit()
    else:
        return jsonify(constants.NOTE_UNACCESSABLE), 402

    return jsonify(constants.EDITOR_DELETED), 200


@app.route(BASE_PATH + EDITOR_PATH + NOTE_PATH + '/all_notes' + '/' + '<int:note_id>', methods=['GET'])
@auth.login_required
def get_all_note_editors(note_id):
    user = auth.current_user()
    try:
        editors = session.query(ForeignEditor).filter_by(note_id=int(note_id)).all()
    except:
        editors = []

    editors_dto = ForeignEditorSchema(many=True)
    note = session.query(Note).filter_by(id=int(note_id)).one()
    if user.id == note.owner_id:
        return jsonify(editors_dto.dump(editors)), 200
    else:
        return jsonify(constants.NOTE_UNACCESSABLE), 402


if __name__ == '__main__':
    app.run()
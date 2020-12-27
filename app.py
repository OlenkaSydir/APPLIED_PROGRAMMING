from flask import Flask, request
from models import Session, User, Note, ForeignEditor
import utils
import constants
from constants import USER_PATH, BASE_PATH
from schemas import UserSchema
from flask import jsonify

app = Flask("__name__")

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

@app.route(BASE_PATH + USER_PATH + '/' + '<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    print(user_id)
    try:
        user = session.query(User).filter_by(id=int(user_id)).one()

    except:
        return jsonify(constants.USER_NOT_FOUND), 404

    return jsonify(UserSchema().dump(user)), 200

@app.route(BASE_PATH + USER_PATH + '/' + '<int:user_id>', methods=['PUT'])
def update_user(user_id):

    update_request = request.get_json()

    try:
        user = session.query(User).filter_by(id=int(user_id)).one()
    except:
        return jsonify(constants.USER_NOT_FOUND), 404

    update_user = utils.update_util(user, update_request)

    if update_user == None:
        return jsonify(constants.SOMETHING_WENT_WRONG), 400

    return jsonify(constants.USER_UPDATED), 200

@app.route(BASE_PATH + USER_PATH + '/' + '<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    try:
        user = session.query(User).filter_by(id=int(user_id)).one()
    except:
        return jsonify(constants.USER_NOT_FOUND), 404

    try:
        notes = session.query(Note).filter_by(owner_id=int(user_id)).all()
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


if __name__ == '__main__':
    app.run()
from flask import Flask, request
from models import Session, User
import utils
import constants

app = Flask("__name__")

session = Session()

@app.route('/api/v1/hello-world-<int:var>')
def hello_world(var):
    return 'Hello World ' + str(var)


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    user_request = request.get_json()
    email = user_request['email']

    if utils.find_by_email(email) != None:
        return constants.USER_ALREADY_EXISTS, 400

    user = User(**user_request)
    session.add(user)
    session.commit()

    return constants.USER_CREATED, 201







if __name__ == '__main__':
    app.run()
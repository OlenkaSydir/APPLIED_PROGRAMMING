from models import Session, User

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

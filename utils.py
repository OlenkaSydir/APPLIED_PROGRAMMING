from models import Session, User

session = Session()


def find_by_email(email):
    try:
        user = session.query(User).filter_by(email=email).one()
    except:
        return None
    return user

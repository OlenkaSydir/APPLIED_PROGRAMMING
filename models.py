from sqlalchemy import create_engine, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy import Column, orm
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:example@localhost:5432/note_maker')
Base = declarative_base()
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    password = Column(String)
    email = Column(String)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    title = Column(String)

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    note_text = Column(String)
    owner_id = Column(Integer, ForeignKey(User.id))
    tag_id = Column(Integer, ForeignKey(Tag.id))

    owner = orm.relationship(User, backref = "notes", lazy = "joined")
    tag = orm.relationship(Tag, backref = "tags", lazy = "joined")

class Edit(Base):
    __tablename__ = "edits"
    id = Column(Integer, primary_key=True)
    editor_id = Column(Integer)
    note_id = Column(Integer)
    edit_timestamp = Column(TIMESTAMP)

class ForeignEditor(Base):
    __tablename__ = "foreign_editors"
    id = Column(Integer, primary_key=True)
    editor_id = Column(Integer)
    note_id = Column(Integer)
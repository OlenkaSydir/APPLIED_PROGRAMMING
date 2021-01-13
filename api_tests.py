import unittest
from app import app
from base64 import b64encode
import sqlalchemy
import json
from models import engine


class TestBase(unittest.TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app
    tester = app.test_client()
    creds = b64encode(b"lina:1111").decode('utf-8')
    creds2 = b64encode(b"linka:111").decode('utf-8')
    randomcreds = b64encode(b"abc:dfg").decode('utf-8')


class UserApitest(TestBase):
    data = {
        "user_name": "lina",
        "password": "1111",
        "email": "lina@gmail.com"
    }

    def test_create_user(self):
        cleanBase()
        response = self.tester.post("/api/v1/users", data=json.dumps(self.data), content_type="application/json")
        code = response.status_code
        self.assertEqual(201, code)

    def test_find_user_by_id(self):
        cleanBase()
        add_user()
        response = self.tester.get('/api/v1/users/me', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_if_authorised_user(self):
        cleanBase()
        add_user()
        response = self.tester.get('/api/v1/users/me', headers={"Authorization": f"Basic {self.randomcreds}"})
        code = response.status_code
        self.assertEqual(401, code)

    def test_update(self):
        cleanBase()
        add_user()
        response = self.tester.put('/api/v1/users/update_me',
                                   data=json.dumps({"user_name": "linka", "password": 111}),
                                   content_type='application/json',
                                   headers={"Authorization": f"Basic {self.creds}"})

        code = response.status_code
        self.assertEqual(200, code)


    def test_all_users(self):
        response = self.tester.get('/api/v1/users')
        code = response.status_code
        self.assertEqual(200, code)

    def test_delete_user(self):
        cleanBase()
        add_user()
        response = self.tester.delete('/api/v1/users/delete_me', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)


class NoteApiTest(TestBase):
    note_data = {
        "id": 1,
        "note_text": "hello world!",
        "owner_id": 1,
        "tag_title": "hello"
    }

    def test_create_note(self):
        cleanBase()
        add_user()
        response = self.tester.post('/api/v1/notes/add_my_note', data=json.dumps(self.note_data),
                                    content_type='application/json',
                                    headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(201, code)

    def test_all_notes(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        response = self.tester.get('/api/v1/notes')
        code = response.status_code
        self.assertEqual(200, code)

    def test_edit_note(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        response = self.tester.put('/api/v1/notes/1', data=json.dumps({"note_text": "helloooooo"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_edit_note_invalid(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        response = self.tester.put('/api/v1/notes/3', data=json.dumps({"note_text": "helloooooo"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_get_all_notes_of_a_user(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        response = self.tester.get('/api/v1/notes/users/my_notes',  headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_find_note_by_id(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        response = self.tester.get('/api/v1/notes/1', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_find_note_by_id_invalid(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        response = self.tester.get('/api/v1/notes/4', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_delete_note_by_id(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        response = self.tester.delete('/api/v1/notes/1', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_delete_note_by_invalid_id(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        response = self.tester.delete('/api/v1/notes/4', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(400, code)



class EditorApiTests(TestBase):
    def test_add_editor(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        response = self.tester.post('/api/v1/editors/add_foreign_editor', data=json.dumps({"editor_id": 2, "note_id": 1}),
                                    content_type='application/json',
                                    headers={"Authorization": f"Basic {self.creds}"})

        code = response.status_code
        self.assertEqual(201, code)

    def test_add_bad_editor(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        response = self.tester.post('/api/v1/editors/add_foreign_editor', data=json.dumps({"editor_id": 3, "note_id": 1}),
                                    content_type='application/json',
                                    headers={"Authorization": f"Basic {self.creds}"})

        code = response.status_code
        self.assertEqual(404, code)

    def test_add_editor_again(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        add_editor()
        response = self.tester.post('/api/v1/editors/add_foreign_editor', data=json.dumps({"editor_id": 1, "note_id": 1}),
                                    content_type='application/json',
                                    headers={"Authorization": f"Basic {self.creds}"})

        code = response.status_code
        self.assertEqual(400, code)


    def test_add_too_many_editors(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        add_6_editors()
        response = self.tester.post('/api/v1/editors/add_foreign_editor',data=json.dumps({"note_id": 1}),
                                    content_type='application/json',
                                    headers={"Authorization": f"Basic {self.creds}"})

        code = response.status_code
        self.assertEqual(404, code)

    def test_delete_editor(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        add_editor()
        response = self.tester.delete('/api/v1/editors/1/notes/1',
                                    headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_delete_editor_invalid_note(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        add_editor()
        response = self.tester.delete('/api/v1/editors/1/notes/3',
                                    headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_delete_invalid_editor(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        add_editor()
        response = self.tester.delete('/api/v1/editors/7/notes/1',
                                    headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_all_note_editors(self):
        cleanBase()
        add_user()
        add_tag()
        add_note()
        add_editor()
        response = self.tester.get('/api/v1/editors/notes/all_notes/1',
                                      headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)



def cleanBase():
    file = open("E:\\Лапітєх\\aplied_programming\\flaskProject\\cleanDB.sql")
    insert = sqlalchemy.text(file.read())
    engine.execute(insert)
    file.close()


def add_user():
    insert_file = open('E:\\Лапітєх\\aplied_programming\\flaskProject\\add_user.sql')
    insert = sqlalchemy.text(insert_file.read())
    engine.execute(insert)
    insert_file.close()


def add_tag():
    insert_file = open('E:\\Лапітєх\\aplied_programming\\flaskProject\\add_tag.sql')
    insert = sqlalchemy.text(insert_file.read())
    engine.execute(insert)
    insert_file.close()

def add_note():
    insert_file = open('E:\\Лапітєх\\aplied_programming\\flaskProject\\add_note.sql')
    insert = sqlalchemy.text(insert_file.read())
    engine.execute(insert)
    insert_file.close()

def add_6_editors():
    insert_file = open('E:\\Лапітєх\\aplied_programming\\flaskProject\\add_6_editors.sql')
    insert = sqlalchemy.text(insert_file.read())
    engine.execute(insert)
    insert_file.close()

def add_editor():
    insert_file = open('E:\\Лапітєх\\aplied_programming\\flaskProject\\add_editor.sql')
    insert = sqlalchemy.text(insert_file.read())
    engine.execute(insert)
    insert_file.close()


if __name__ == '__main__':
    unittest.main()
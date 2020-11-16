# flask_project
## Instalation

Use the package manager pip to install pyenv.
bash
pip install pyenv

Use the package manager pyenv to install python.
bash
pyenv install 3.7.7

Use the package manager pip to install pipenv.
bash
pip install --user pipenv
Use the package manager pip to install flask.
bash
pip install flask
## Waitress
Install waitress in pipenv
bash
pipenv install waitress
## Usage
bash
from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route('/')
def homepage():
    return 'copy and paste this to url: /api/v1/hello-world- and enter the number'


@app.route('/api/v1/hello-world-<int:var>')
def hello_world(var):
    return 'Hello World-' + str(var)


if __name__ == '__main__':
    # app.run()
    serve(app, port=4656)

## Running with gunicorn
 bash
python app.py

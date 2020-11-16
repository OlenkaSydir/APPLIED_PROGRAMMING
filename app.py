from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route('/')
def homepage():
    return 'copy and paste this to url: /api/v1/hello-world- and enter the number'


@app.route('/api/v1/hello-world-<int:var>')
def hello_world(var):
    return 'Hello World ' + str(var)


if __name__ == '__main__':
    # app.run()
    serve(app, port=4656)

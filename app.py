from flask import Flask
from waitress import serve
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self, name):
        return {"data": "Hello " + name}

    def post(self):
        return {"data": "posted"}


api.add_resource(HelloWorld, "/longhw/<string:name>")


@app.route('/')
def homepage():
    return 'copy and paste this to url: /api/v1/hello-world- and enter the number'


@app.route('/api/v1/hello-world-<int:var>')
def hello_world(var):
    return 'Hello World ' + str(var)


if __name__ == '__main__':
    # app.run()
    serve(app, port=4656)

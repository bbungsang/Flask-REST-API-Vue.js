import os
import json

from flaskext.mysql import MySQL
from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
api_secret_keys = json.loads(open(os.path.join(BASE_DIR, 'api_secret_keys.json')).read())


app = Flask(__name__)
api = Api(app)

# mysql 연결
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = api_secret_keys['mysql']['user']
app.config['MYSQL_DATABASE_PASSWORD'] = api_secret_keys['mysql']['password']
app.config['MYSQL_DATABASE_DB'] = api_secret_keys['mysql']['db_name']
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("select * from nonsense_quiz")
data = cursor.fetchall()

items_list = []

for item in data:
    i = {
        "id": item[0],
        "question": item[1],
        "answer": item[2],
        "hint": item[3]
    }
    items_list.append(i)


class Test(Resource):
    def get(self):
        return i

api.add_resource(Test, '/create/quiz')

if __name__ == '__main__':
    app.run(debug=True)

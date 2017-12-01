import os
import json

from flaskext.mysql import MySQL
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
api_secret_keys = json.loads(open(os.path.join(BASE_DIR, 'api_secret_keys.json')).read())

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'

# mysql 연결
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = api_secret_keys['mysql']['user']
app.config['MYSQL_DATABASE_PASSWORD'] = api_secret_keys['mysql']['password']
app.config['MYSQL_DATABASE_DB'] = api_secret_keys['mysql']['db_name']
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

class NonsenseQuiz(Resource):
    def get(self):
        cursor.execute("SELECT * FROM nonsense_quiz")
        data = cursor.fetchall()

        result = []
        columns = "id", "question", "answer", "hint"

        for row in data:
            result.append(dict(zip(columns, row)))
        return result

    def post(self):
        question = request.form['question']
        answer = request.form['answer']
        hint = request.form['hint']

        query = "INSERT INTO nonsense_quiz \
        (question, answer, hint) VALUES \
        ('" + question + "', '" + answer + "', '" + hint + "');"
        cursor.execute(query)
        conn.commit();

        return "success"

api.add_resource(NonsenseQuiz, '/api/quiz')

if __name__ == '__main__':
    app.run(debug=True)

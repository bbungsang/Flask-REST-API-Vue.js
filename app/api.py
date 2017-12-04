import os
import json

from flaskext.mysql import MySQL
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
api_secret_keys = json.loads(open(os.path.join(BASE_DIR, 'api_secret_keys.json')).read())

app = Flask(__name__)
api = Api(app)

# CORS 설정
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# MySQL 연결
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = api_secret_keys['mysql']['user']
app.config['MYSQL_DATABASE_PASSWORD'] = api_secret_keys['mysql']['password']
app.config['MYSQL_DATABASE_DB'] = api_secret_keys['mysql']['db_name']
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


class SolveQuiz(Resource):
    """ 넌센스 퀴즈 보기 및 풀기 """

    def get(self, q_id):
        cursor.execute("SELECT * FROM nonsense_quiz")
        last_q = len(cursor.fetchall())

        cursor.execute("SELECT * FROM nonsense_quiz WHERE id=" + q_id)
        data = cursor.fetchall()

        columns = "id", "question", "answer", "hint"
        result = dict(zip(columns, data[0]))
        result.update({"last_q": last_q})

        return result

    def post(self, q_id):
        cursor.execute("SELECT * FROM nonsense_quiz WHERE id=" + q_id)
        data = cursor.fetchall()

        db_answer = data[0][2]
        result = request.data.decode("utf-8")

        if db_answer != result[1:-1].split(":")[1][1:-1]:
            return {
                "check": "틀렸습니다",
                "next": False
            }

        return {
            "check": "정답입니다",
            "next": True
        }


class CreateQuiz(Resource):
    """ 퀴즈 추가하기 """

    def post(self):
        s = request.data.decode("utf-8")
        result = json.loads(s.replace("'", "\""))
        question = result['question']
        answer = result['answer']
        hint = result['hint']
        query = "INSERT INTO nonsense_quiz \
        (question, answer, hint) VALUES \
        ('" + question + "', '" + answer + "', '" + hint + "');"
        cursor.execute(query)
        conn.commit();
        return "success"

api.add_resource(SolveQuiz, '/api/solve/<q_id>')
api.add_resource(CreateQuiz, '/api/create/')

if __name__ == '__main__':
    app.run(debug=True)
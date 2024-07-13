from flask import Flask, request, json, Response
from flask_sqlalchemy import SQLAlchemy
import time
from request_subscribers import receive_subscribers_from_groups
from queue import Queue
import threading
import multiprocessing
import asyncio

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
queue = Queue(maxsize=1)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), unique=True, nullable=False)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(80), unique=True, nullable=False)
    api_id = db.Column(db.String(80), unique=False, nullable=False)
    api_hash = db.Column(db.String(200), unique=False, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=True)

@app.route('/')
def group_page():
    try:
        groups_json = [{'id': g.id, 'url': g.url} for g in Group.query.all()]
        return json.dumps(groups_json)
    except:
        print("error while sending groups through API")
        return Response(status=501)

@app.route("/add_group", methods=["POST"])
def add_group():
    try:
        data = json.loads(request.data)
        new_group = Group(url=data["url"])
        db.session.add(new_group)
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД group!")
        return Response(status=501)
    return Response(status=200)


@app.route('/accounts')
def account_page():
    try:
        accounts_json = [{'id': a.id, 'phone_number': a.phone_number, 'api_id': a.api_id, 'api_hash': a.api_hash, 'password': a.password} for a in Account.query.all()]
        return json.dumps(accounts_json)
    except:
        print("error while sending accounts through API")
        return Response(status=501)

@app.route("/add_account", methods=["POST"])
def add_account():
    try:
        data = json.loads(request.data)
        new_account = Account(phone_number=data["phone_number"], api_id=data["api_id"], api_hash=data["api_hash"], password=data["password"])
        db.session.add(new_account)
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД account!")
        return Response(status=501)
    return Response(status=200)

@app.route("/post_telegram_code", methods=["POST"])
def post_code():
    try:
        data = json.loads(request.data)
        queue.put(data["code"])

        return Response(status=200)
    except:
        print("Ошибка получения telegram code!")
        return Response(status=501)


def start_web_server():
    with app.app_context():
        db.create_all()

    app.run(debug = True)

def main():
    loop = asyncio.get_event_loop()
    thr = threading.Thread(target=receive_subscribers_from_groups, args=(queue, loop)).start()
    start_web_server()
    thr.join()

if __name__ == '__main__':
    main() 










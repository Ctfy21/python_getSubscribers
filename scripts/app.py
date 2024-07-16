import multiprocessing
from flask import Flask, request, json, Response, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import create_engine

from db_repository import get_accounts_repository
from request_subscribers import main_receive_cycle


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

from db_repository import metadata, Group, Account
db = SQLAlchemy(metadata=metadata)

code_queue = multiprocessing.Queue(maxsize=1)

restart_flag = multiprocessing.Event()

@app.route('/')
def group_page():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"error while getting groups through API: error - {e}")
        return Response(status=501)

@app.route('/get_groups', methods=["GET"])
def get_groups():
    try:
        groups_json = [{'id': g.id, 'url': g.url} for g in db.session.query(Group).all()]
        return json.dumps(groups_json)
    except Exception as e:
        print(f"error while getting groups through API: error - {e}")
        return Response(status=501)
    
@app.route("/add_group", methods=["POST"])
def add_group():
    try:
        data = json.loads(request.data)
        new_group = Group(url=data["url"], subscribers=None)
        db.session.add(new_group)
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД group!")
        return Response(status=501)
    return Response(status=200)

@app.route("/delete_group", methods=["DELETE"])
def delete_group():
    try:
        data = json.loads(request.data)
        group = db.session.query(Group).filter_by(url=data["url"]).first()
        db.session.delete(group)
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка удаления в БД group!")
        return Response(status=501)
    return Response(status=200)


@app.route('/account', methods=["GET"])
def account_page():
    try:
        return render_template('account.html')
    except:
        print("error while getting account_page")
        return Response(status=501)

@app.route('/get_account')
def get_account():
    try:
        accounts_json = [{'id': a.id, 'phone_number': a.phone_number, 'api_id': a.api_id, 'api_hash': a.api_hash, 'password': a.password, 'result_send_chat': a.result_send_chat} for a in db.session.query(Account).all()]
        return json.dumps(accounts_json)
    except:
        print("error while getting accounts through API")
        return Response(status=501)

@app.route("/add_account", methods=["POST"])
def add_account():
    try:
        data = json.loads(request.data)
        new_account = Account(phone_number=data["phone_number"], api_id=data["api_id"], api_hash=data["api_hash"], password=data["password"], result_send_chat=data["result_send_chat"])
        db.session.add(new_account)
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД account!")
        return Response(status=501)
    
    def restart_cycle():
        engine = create_engine("sqlite:///instance/main.db")
        accounts = [account for account in get_accounts_repository(engine)]

        if(len(accounts) > 1):
            restart_flag.clear()
            restart_flag.wait()

        multiprocessing.Process(target=main_receive_cycle, args=(code_queue, accounts, restart_flag)).start()
        print("restart cycle")

    response = Response(status=200)
    response.call_on_close(restart_cycle())
    return response

@app.route("/delete_account", methods=["DELETE"])
def delete_account():
    try:
        data = json.loads(request.data)
        account = db.session.query(Account).filter_by(phone_number=data["phone_number"]).first()
        db.session.delete(account)
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка удаления в БД account!")
        return Response(status=501)
    
    def restart_cycle():
        restart_flag.clear()
        restart_flag.wait()

        engine = create_engine("sqlite:///instance/main.db")
        accounts = [account for account in get_accounts_repository(engine)]
        multiprocessing.Process(target=main_receive_cycle, args=(code_queue, accounts, restart_flag)).start()
        print("restart cycle")

        
    response = Response(status=200)
    response.call_on_close(restart_cycle())
    return response

@app.route("/post_telegram_code", methods=["POST"])
def post_code():
    try:
        data = json.loads(request.data)
        code_queue.put(data["code"])

        return Response(status=200)
    except:
        print("Ошибка получения telegram code!")
        return Response(status=501)


def start_server():

    db.init_app(app)
    with app.app_context():
        db.create_all()

    engine = create_engine("sqlite:///instance/main.db")
    accounts = [account for account in get_accounts_repository(engine)]

    multiprocessing.Process(target=main_receive_cycle, args=(code_queue, accounts, restart_flag)).start()

    app.run(use_reloader=False)


if __name__ == "__main__":
    start_server()








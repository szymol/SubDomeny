from flask import Flask, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from sqlalchemy import text

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://subdom2018:subdom2018@subdom2018.cfijc6ozllle.eu-central-1.rds.amazonaws.com:1433/subdom2018'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

class Users(db.Model):
    __tablename_ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    login = db.Column('login', db.Unicode)
    password = db.Column('password', db.Unicode)
    email = db.Column('email', db.Unicode)

    def __init__(self, login, password, email):
        self.login = login
        self.password = password
        self.email = email

class Subdomains(db.Model):
    __tablename__ = 'subdomains'
    id = db.Column('id_domain', db.Integer, primary_key=True)
    id_u = db.Column('id_user', db.Integer)
    name = db.Column('name', db.Unicode)
    at = db.Column('at', db.Unicode)
    ip_a = db.Column('ip_adress', db.Unicode)

    def __init__(self, id_u, name, at, ip_a):
        self.id_u = id_u
        self.name = name
        self.at = at
        self.ip_a = ip_a


def say_hello():
    sql = text('select * from users')
    result = db.engine.execute(sql)
    names = []
    for row in result:
        names.append(row[1])
    names2 = json.dumps(names)
    return jsonify(test=names2)

def existing_subdomains():
    query = text('select * from subdomains')
    result = db.engine.execute(query)
    names = []
    for row in result:
        names.append(row[2] + '.' + row[3])
    names2 = json.dumps(names)
    return jsonify(subdomains=names2)

def add_user(username):
    update_this = Users.query.filter_by(email='Kaminarious@thunder.jp').first()
    if update_this:
        try:
            update_this.login = username
            db.session.commit()
            return('successfully updated the login to ' + str(username) +'!')
        except Exception as e:
            print(e)
    else:
        new_user = Users(username, 'zappityzap', 'Kaminarious@thunder.jp')
        try:
            db.session.add(new_user)
            db.session.commit()
            return('successfully created new user!')
        except Exception as e:
            print(e)

application.add_url_rule('/', 'index', (lambda:
    say_hello()))

application.add_url_rule('/subdomains/', 'subdomains', (lambda:
    existing_subdomains()))

application.add_url_rule('/add/<username>', 'hello', (lambda username:
    add_user(username)))


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

from flask import Flask, jsonify, json, request
from flask.views import MethodView
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

class API_Users(MethodView):
    def get(self, user_id):
        if user_id is None:
            sql = text('select * from users')
            result = db.engine.execute(sql)
            names = []
            for row in result:
                names.append(row[1])
            names2 = json.dumps(names)
            return jsonify(test=names2)
        else:
            sql = text('select * from users where id = ' + str(user_id))
            result = db.engine.execute(sql)
            names = []
            for row in result:
                names.append(row[1])
            names2 = json.dumps(names)
            return jsonify(test=names2)

    def post(self):
        return str(request.get_json()['login'])

    def delete(self, user_id):
        return 'delete user with id == ' + str(user_id)

    def put(self, user_id):
        return 'update user with id == ' + str(user_id)




user_view = API_Users.as_view('user_api')
application.add_url_rule('/users/', defaults={'user_id':None},view_func=user_view, methods=['GET'])
application.add_url_rule('/users/',view_func=user_view, methods=['POST'])
application.add_url_rule('/users/<int:user_id>',view_func=user_view, methods=['GET','PUT','DELETE'])

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
	
'''
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

from flask import Flask, jsonify, render_template, url_for, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://subdom2018:subdom2018@subdomdb.casm6gqak8bd.us-east-2.rds.amazonaws.com:5432/subdomdb'
api = Api(app)
db = SQLAlchemy(app)


def application(environ, start_response):
    path    = environ['PATH_INFO']
    method  = environ['REQUEST_METHOD']
    if method == 'GET':
        try:
            if path == '/':
                response = 'index'
            elif path == '/scheduled':
                response = 'hewwo scheduleeee'
        except (TypeError, ValueError):
            response = 'Error retrieving request body for async work.'
    else:
        response = 'hewwo'
    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)
    return [response]


if __name__ == '__main__':
    app.run(host = '0.0.0.0')
'''

from flask import Flask, jsonify, json, request
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from sqlalchemy import text
#import psycopg2


application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://subdom2018:subdom2018@subdom2018.cfijc6ozllle.eu-central-1.rds.amazonaws.com:1433/subdom2018'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

#################
### db models ###
#################

class Users(db.Model):
    __tablename_ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    login = db.Column('login', db.Unicode)
    password = db.Column('password', db.Unicode)
    email = db.Column('email', db.Unicode)
    last_login_date = db.Column('last_login_date', db.Date)
    registration_date = db.Column('registration_date', db.Date)
    subdomains = db.relationship('Subdomains', backref='user', lazy=True)

    def __init__(self, login, password, email, last_login_date, registration_date, subdomains):
        self.login = login
        self.password = password
        self.email = email
        self.last_login_date = last_login_date
        self.registration_date = registration_date
        self.subdomains = subdomains

class Subdomains(db.Model):
    __tablename = 'subdomains'
    id_domain = db.Column('id_domain', db.Integer, primary_key = True)
    id_user = db.Column('id_user', db.Integer, db.ForeignKey('users.id'))
    name = db.Column('name', db.Unicode)
    at = db.Column('at', db.Unicode)
    ip_address = db.Column('ip_address', db.Unicode)
    purchase_date = db.Column('purchase_date', db.Date)
    expiration_date = db.Column('expiration_date', db.Date)
    status = db.Column('status', db.Unicode)


    def __init__(self, id_user, name, at, ip_address, purchase_date, expiration_date, status):
        self.id_user = id_user
        self.name = name
        self.at = at
        self.ip_address = ip_address
        self.purchase_date = purchase_date
        self.expiration_date = expiration_date
        self.status = status

class Address(db.Model):
    __tablename = 'addresses'
    id = db.Column('id', db.Integer, primary_key = True)
    id_user = db.Column('id_user', db.Integer, db.ForeignKey('users.id'))
    country = db.Column('country', db.Unicode)
    state = db.Column('state', db.Unicode)
    city = db.Column('city', db.Unicode)
    street = db.Column('street', db.Unicode)
    house_nr = db.Column('house_nr', db.Integer)
    apartment_nr = db.Column('apartment_nr', db.Unicode)
    postal_code = db.Column('postal_code', db.Integer)

    def __init__(self, id_user, country, state, city, street, house_nr, apartment_nr, postal_code):
        self.id_user = id_user
        self.country = country
        self.state = state
        self.city = city
        self.street = street
        self.house_nr = house_nr
        self.apartment_nr = apartment_nr
        self.postal_code = postal_code

################
### API func ###
################

class API_Users(MethodView):
    def get(self, user_id):
        if user_id is None:
            count = db.engine.execute("select count(id) from users")
            count2 = count.fetchall()
            count = count2[0][0]
            result = db.engine.execute("select * from users")
            row = result.fetchall()
            list = []
            for i in range(count):
                subdom_dict = {
                    'id' : row[i][0],
                    'login' : row[i][1],
                    'password' : row[i][2],
                    'email' : row[i][3],
                    'last_login_date' : str(row[i][4]),
                    'registration_date' : str(row[i][5])}
                list.append(subdom_dict)
            
            return json.dumps(list)

        else:
            result = db.engine.execute("select * from users where id = '" + str(user_id) + "'")
            row = result.fetchall()
            subdom_dict = {
                'id' : row[0][0],
                'login' : row[0][1],
                'password' : row[0][2],
                'email' : row[0][3],
                'last_login_date' : str(row[0][4]),
                'registration_date' : str(row[0][5])}
            
            return json.dumps(subdom_dict)

    def post(self):
        return str(request.get_json()['login'])

    def delete(self, user_id):
        return 'delete user with id == ' + str(user_id)

    def put(self, user_id):
        columns = request.get_json()['columns']
        values = request.get_json()['values']
        string = "UPDATE users SET "
        for i in range (len(columns) - 1):
            string = string \
                    + str(columns[i]) \
                    + " = '" + str(values[i]) \
                    + "', "
        string = string \
                + str(columns[len(columns) - 1]) \
                + " = '" + str(values[len(columns) - 1]) \
                + "' WHERE id = " \
                + str(user_id)
        result = db.engine.execute(string)
        return json.dumps({'message' : 'success'})

class API_Subdomains(MethodView):
    def get(self,user_id):
        if user_id is None:
            count = db.engine.execute("select count(id_domain) from subdomains")
            count2 = count.fetchall()
            count = count2[0][0]
            result = db.engine.execute("select * from subdomains")
            row = result.fetchall()
            list = []
            for i in range(count):
                subdom_dict = {
                    'id_domain' : row[i][0],
                    'id_user' : row[i][1],
                    'name' : row[i][2],
                    'at' : row[i][3],
                    'ip_address' : row[i][4],
                    'purchase_date' : str(row[i][5]),
                    'expiration_date' : str(row[i][6]),
                    'status' : row[i][7]}
                list.append(subdom_dict)
            
            return json.dumps(list)

        else:
            count = db.engine.execute("select count(id_domain) from subdomains WHERE id_user = '" + str(user_id) + "'")
            count2 = count.fetchall()
            count = count2[0][0]
            result = db.engine.execute("select * from subdomains WHERE id_user = '" + str(user_id) + "'")
            row = result.fetchall()
            list = []
            for i in range(count):
                subdom_dict = {
                    'id_domain' : row[i][0],
                    'id_user' : row[i][1],
                    'name' : row[i][2],
                    'at' : row[i][3],
                    'ip_address' : row[i][4],
                    'purchase_date' : str(row[i][5]),
                    'expiration_date' : str(row[i][6]),
                    'status' : row[i][7]}
                list.append(subdom_dict)
            
            return json.dumps(list)

    def post(self):
        id_user = request.get_json()['id_user']
        name = request.get_json()['name']
        at = request.get_json()['at']
        ip_address = request.get_json()['ip_address']
        purchase_date = request.get_json()['purchase_date']
        expiration_date = request.get_json()['expiration_date']

        new_subdom = Subdomains(id_user, name, at, ip_address, purchase_date, expiration_date, 'ACTIVE')
        db.session.add(new_subdom)
        db.session.commit()

        return json.dumps({'message' : 'success'})

    def put(self, subdomain_id):
        columns = request.get_json()['columns']
        values = request.get_json()['values']
        string = "UPDATE subdomains SET "
        for i in range (len(columns) - 1):
            string = string \
                    + str(columns[i]) \
                    + " = '" + str(values[i]) \
                    + "', "
        string = string \
                + str(columns[len(columns) - 1]) \
                + " = '" + str(values[len(columns) - 1]) \
                + "' WHERE id_domain = " \
                + str(subdomain_id)
        result = db.engine.execute(string)
        
        return json.dumps({'message' : 'success'})


##############
### routes ###
##############
user_view = API_Users.as_view('user_api')
subdom_view = API_Subdomains.as_view('sub_api')
application.add_url_rule('/users/', defaults={'user_id':None},view_func=user_view, methods=['GET'])
application.add_url_rule('/users/',view_func=user_view, methods=['POST'])
application.add_url_rule('/users/<int:user_id>',view_func=user_view, methods=['GET','PUT','DELETE'])
application.add_url_rule('/users/<int:user_id>/subdomains/', view_func=subdom_view, methods=['GET'])
application.add_url_rule('/subdomains/', defaults={'user_id':None},view_func=subdom_view, methods=['GET'])
application.add_url_rule('/subdomains/',view_func=subdom_view, methods=['POST'])
application.add_url_rule('/subdomains/<int:subdomain_id>',view_func=subdom_view, methods=['PUT'])


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

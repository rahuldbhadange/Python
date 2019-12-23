from flask import Flask, request, make_response, abort
# from  flask import g, jsonify
# # from . import api
# import jwt
# import datetime
# from functools import wraps

app = Flask(__name__)


#app.config['SECRET_KEY'] = 'asdf'


@app.route('/hi', methods=['GET'])
def api_all():
    return 'hello'


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return make_response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/login', methods=['GET'])
def requires_auth():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):  # no header set
        return authenticate()
    # user = api.query.filter_by(username=auth.username).first()
    # if user is None or user.password != auth.password:
        #abort(401)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

























'''


@app.route('/unprotected')
def unprotected():
    return ''


@app.route('/protected')
def protected():
    return ''
    
    
    if auth and auth.password == 'password' and auth and auth.username == 'username':
        token = jwt.encode({'user':auth.password, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'www-Authenticate': 'Basic realm="Login Required"'})



@app.verify_password
def verify_password(usr, pwd):
    user = User.query.filter_by(usr=usr).first()
    if not user or not user.verify_password(pwd):
        return False
    g.user = user
    return True
    
    
@app.route('/sapwarrantyrecall', methods = ['POST'])
def new_user():
    username = request.json.get('usr')
    password = request.json.get('pwd')
    if username is None or password is None:
        return "<h1>404</h1><p>Username Password required.</p>", 404  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        return "<h1>404</h1><p>Username Password required.</p>", 404  # existing user
    user = User(username = username)
    user.hash_password(password)
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}
'''
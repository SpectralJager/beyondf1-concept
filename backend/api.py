import re
from flask import Blueprint, request, jsonify, make_response
from hashlib import sha512
import jwt, psycopg2, json, datetime

# secret key
secret_key = b'Some_supsdlfahskleajr;lkfajs;ldkfhna;sjkfdahsldkfjnaskljh29883rfhsahljk'
# api blueprints
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api_v1')

def connectToDatabase():
    try:
        connection = psycopg2.connect(
            user = "postgres",
            password = "238516",
            host = "127.0.0.1",
            port = "5432",
            database = "beyondf1"
        )
        cursor = connection.cursor()
        return cursor, connection
    except Exception as e:
        print("[#] Error with connection to PostgreSQL!\n", e)
        return None

# auth api
@api_v1.route('/auth/check_token', methods=['POST'])
def check_token():
    try:
        decode_token = jwt.decode(request.json['token'], secret_key, algorithms=['HS256'])
        response = {
            'message': 'Valid token!',
            'code': 'success'
        }
    except jwt.ExpiredSignatureError:
        response = {
            'message': 'Token expired!',
            'code': 'warning'
        }
    except jwt.InvalidTokenError:
        response = {
            'message': 'Token Invalid!',
            'code': 'danger'
        }
    return make_response(response, 200)

@api_v1.route('/auth/login', methods=['POST'])
def auth_login():
    # get login data from site
    username = request.json['username']
    password = request.json['password']
    # hash password
    password = sha512(bytes(password.encode('utf-8'))).hexdigest()
    # get cursor
    cursor, _ = connectToDatabase()
    # get admin by username
    cursor.execute("SELECT * FROM admins WHERE username = %r;" % username)
    admin = cursor.fetchone()
    if admin and password == admin[3]:
        # if data correct, create token and confirm login
        response = {
            'message': 'Correct data, happy hacking!',
            'jwt': jwt.encode({'username': admin[1], 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10)}, secret_key, algorithm="HS256", ),
            'code': 'success'
        }
    else:
        response = {
            'message': 'Data incorect or missing!',
            'code': 'warning'
        }
    return make_response(response, 200)

@api_v1.route('/auth/register', methods=['POST'])
def auth_register():
    # get register data
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    password = sha512(bytes(password.encode('utf-8'))).hexdigest()
    # get acces to db
    cursor, connection = connectToDatabase()
    # check is availiable username
    try:
        cursor.execute("SELECT * FROM admins WHERE username = %r" % username)
        username_res = cursor.fetchone()
        # check is availiable email
        cursor.execute("SELECT * FROM admins WHERE email = %r" % email)
        email_res = cursor.fetchone()

        if username_res and email_res:
            response = {
                'message': 'Username or email not accetable',
                'code': 'warning'
            }
        else:
            cursor.execute("INSERT INTO admins ( username, email, password) VALUES ( %r, %r, %r);" % (username, email, password))
            connection.commit()
            response = {
                'message': 'Admin have created!',
                'code': 'success'
            }
    except Exception as e:
        print('[#] Something goes wrong!\n', e)
        response = {
            'message': 'Incorect data!',
            'code': 'danger'
        }
        return make_response(response, 300)
    finally:
        return make_response(response, 200)
    
@api_v1.route('/auth', methods=['PUT','DELETE'])
def auth_delete():
    cursor, connection = connectToDatabase()
    id = request.json['id']
    if request.method == 'DELETE':
        try:
            cursor.execute('DELETE FROM admins where id = %d' % int(id))
            connection.commit()
            response = {
                'message': 'Admin deleted',
                'code': 'success'
            }
        except:
            response = {
                'message': 'Invalid data!',
                'code': 'danger'
            }
    elif request.method == 'PUT':
        try:
            admin = {
                'username': request.json['username'],
                'email': request.json['email'],
                'password': sha512(bytes((request.json['password']).encode('utf-8'))).hexdigest()
            }
            cursor.execute('UPDATE admins set username = %r, email = %r, password = %r WHERE id = %d' % (admin['username'], admin['email'], admin['password'], int(id)))
            connection.commit()
            response = {
                'message': 'Admin updated',
                'code': 'success'
            }
        except:
            response = {
                'message': 'Invalid data',
                'code': 'danger'
            }
    return make_response(response, 200)

# subscribers
@api_v1.route('/subscribers', methods=["GET","POST"])
def subscribers():
    response = {'message': '1'}
    cursor, connection = connectToDatabase()
    if request.method == 'POST':
        email = request.json['email']
        try:
            cursor.execute('INSERT INTO subscribers ( email) VALUES ( %r );' % email)
            connection.commit()
            response = {
                'message': 'New subscriber added!',
                'code': 'success'
            }
        except:
            response = {
                'message': 'Incorect data!',
                'code': 'danger'
            }

    elif request.method == 'GET':
        cursor.execute("SELECT email FROM subscribers;")
        res = cursor.fetchall()
        res = [{
            'email': i[0]
        } for i in res]
        response = {
            'message': 'List of subscribers!',
            'subscribers': res,
            'code': 'success'
        }
    return make_response(response, 200)

@api_v1.route('/subscribers/delete', methods=['DELETE'])
def subscribers_del():
    cursor, connection = connectToDatabase()
    id = request.json['id']
    try:
        cursor.execute('DELETE FROM subscribers where id = %d' % int(id))
        connection.commit()
        response = {
            'message': 'Subscriber deleted',
            'code': 'success'
        }
    except:
        response = {
            'message': 'Invalid data!',
            'code': 'danger'
        }
    return make_response(response, 200)

# articles manipulation
@api_v1.route('/news', methods=['GET','POST'])
def news():
    if request.method == 'POST':
        article = {
            'title': request.json['title'],
            'content': request.json['content'],
            'image_url': request.json['image_url'],
            'created_date': str(datetime.datetime.utcnow())
        }
        cursor, connection = connectToDatabase()
        try:
            cursor.execute('INSERT INTO article (title,content,image_url,created_date) VALUES (%r,%r,%r,%r);' % (article['title'],article['content'],article['image_url'],article['created_date']))
            connection.commit()
            response = {
                'message': 'Article with title %r have added!' % article['title'],
                'code': 'success'
            }
        except Exception as e:
            print('[#] Something goes wrong\n %r' % e)
            response = {
                'message': 'Invalid data!',
                'code': 'danger'
            }
    elif request.method == 'GET':
        n = 8
        p = (request.args.get('page', type=int)) - 1
        cursor, connection = connectToDatabase()
        try:
            cursor.execute("SELECT * FROM article LIMIT {} OFFSET {}".format(n,n*p))
            articles = cursor.fetchall()
            articles = [
                {   
                    'id': i[0],
                    'title': i[1],
                    'content': i[2],
                    'created_date': i[3],
                    'image_url': i[4]
                }
                for i in articles
            ]
            response = {
                'articles': articles,
                'message': f'Articles from {n*p} to {n*p+n}',
                'code': 'success'
            }
        except Exception as e:
            print('[#] Something goes wrong\n %r' % e)
            response = {
                'message': 'Invalid data!',
                'code': 'danger'
            }
    return make_response(response, 200)

@api_v1.route('/news/<int:id>', methods=['PUT', 'GET', 'DELETE'])
def news_by_id(id):
    if request.method == 'PUT':
        article = {
            'id': id,
            'title': request.json['title'],
            'content': request.json['content'],
            'image_url': request.json['image_url'],
        }
        cursor, connection = connectToDatabase()
        try:
            cursor.execute('UPDATE article set title = %r, content = %r, image_url = %r WHERE id = %d' % (article['title'], article['content'], article['image_url'], int(id)))
            connection.commit()
            response = {
                'message': 'Article with id = %d updated' % int(id),
                'code': 'success'
            }
        except Exception as e:
            print('[#] Something goes wrong\n %r' % e)
            response = {
                'message': 'Invalid data!',
                'code': 'danger'
            }
    elif request.method == 'GET':
        cursor, connection = connectToDatabase()
        try:
            cursor.execute("SELECT * FROM article WHERE id = {}".format(int(id)))
            article = cursor.fetchone()
            article = {   
                'id': article[0],
                'title': article[1],
                'content': article[2],
                'created_date': article[3],
                'image_url': article[4]
            }
            response = {
                'article': article,
                'message': 'Articles with id = %d' % int(id),
                'code': 'success'
            }
        except Exception as e:
            print('[#] Something goes wrong\n %r' % e)
            response = {
                'message': 'Invalid data!',
                'code': 'danger'
            }
    if request.method == 'DELETE':
        cursor, connection = connectToDatabase()
        try:
            cursor.execute('DELETE FROM article where id = %d' % int(id))
            connection.commit()
            response = {
                'message': 'Article with id = %d deleted' % id,
                'code': 'success'
            }
        except Exception as e:
            print('[#] Something goes wrong\n %r' % e)
            response = {
                'message': 'Invalid data!',
                'code': 'danger'
            }
    return make_response(response, 200)
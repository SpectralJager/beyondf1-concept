import re
from .models import Article, Admin, db, secret_key
from flask import Blueprint, request, jsonify, make_response
from hashlib import sha512
import jwt, re

# api blueprints
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api_v1')


# auth api
@api_v1.route('/auth/login', methods=['POST'])
def auth_login():
    # get login data from site
    username = request.json['username']
    password = request.json['password']
    # hash password
    password = sha512(bytes(password.encode('utf-8'))).digest()
    # get admin by username
    admin = Admin.query.filter_by(username=username).first()

    if admin and password == admin.password:
        # if data correct, create token and confirm login
        response = {
            'message': 'Correct data, happy hacking!',
            'jwt': jwt.encode({'username': admin.username}, secret_key, algorithm="HS256")
        }
    else:
        response = {
            'message': 'Data incorect or missing!'
        }
    return make_response(response, 200)

@api_v1.route('/auth/register', methods=['POST'])
def auth_register():
    # get register data
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    password = sha512(bytes(password.encode('utf-8'))).digest()

    # check if we have Admin with same username and email
    if Admin.query.filter_by(username = username).first() == None and Admin.query.filter_by(email = email).first() == None:
        # create new Admin
        admin = Admin(username, email, password)
        # save new admin in database
        db.session.add(admin)
        db.session.commit()
        response = {
            'message': 'You have registered'
        }
    else:
        response = {
            'message': 'Incorect data!'
        }


    return make_response(response, 200)
            

    

# news api
@api_v1.route('/news', methods=['GET', 'POST'])
def news():
    print('get request')
    response = {'message': 'Incorect request method!'}
    if request.method == 'GET':
        articles = Article.query.order_by(Article.id.desc()).all()
        if articles:
            response = {
                'articles': [article.json() for article in articles],
                'message': 'success'
            }
        else:
            response = {'message': 'No articles'}
    elif request.method == 'POST':
        title = request.json['title']
        text = request.json['text']
        bg_url = request.json['bg_url']
        domain = request.json['domain']
        source = request.json['source']

        article = Article(title,text,bg_url,domain,source)

        db.session.add(article)
        db.session.commit()

        response = {
            'message': 'Article with name %r added!' % title,
        }
    return make_response(response, 200)

@api_v1.route('/news/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def news_id(id):
    try:
        article = Article.query.get(id)
        if request.method == 'GET':
            response = {'article': article.json(), 'message': 'success'}

        elif request.method == 'PUT':
            article.title = request.json['title']
            article.text = request.json['text']
            article.bg_url = request.json['bg_url']
            article.domain = request.json['domain']
            article.source = request.json['source']
            # update db
            db.session.commit()
            # create responce
            response = {
                'message': 'Article %r with title %r have updated!' % (article.id, article.title), 
            }
        elif request.method == 'DELETE':
            title = article.title
            # update db
            db.session.delete(article)
            db.session.commit()
            # create responce
            response = {
                'message': 'Article with title %r have deleted!' % title, 
            }
    except Exception as e:
        print(e)
        response = {'message': 'Incorect request!'}
    return jsonify(response)
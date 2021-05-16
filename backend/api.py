from .models import Article, db
from flask import Blueprint, request, jsonify, make_response
import sys

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api_v1')

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
        #e = sys.exc_info()[0]
        print(e)
        response = {'message': 'Incorect request!'}
    return jsonify(response)
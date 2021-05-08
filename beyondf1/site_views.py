from flask import render_template, Blueprint
from beyondf1.models import *


#### blueprints
site = Blueprint('site',__name__, template_folder='templates/site')

#### routes
@site.route('/')
def home():
    articles = Article.query.order_by(Article.id.desc())
    return render_template('home.html', articles=articles)

@site.route('/articles/<int:id>/')
def article(id):
    article = Article.query.get(id)
    articles = Article.query.order_by(Article.id.desc())[:2]
    return render_template('article.html', article=article, articles=articles)

@site.route('/wiki')
def wiki():
    return render_template('wiki.html')

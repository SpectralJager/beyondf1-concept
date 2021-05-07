from flask import render_template, Blueprint, request, session, flash, redirect, url_for
from hashlib import sha512
from beyondf1.models import *
from functools import wraps


#### decorators
def is_loggin(f):
    @wraps(f)
    def wrap(*argc, **kwargs):
        if 'is_logged' in session:
            return f(*argc, **kwargs)
        else:
            flash('You need loggin!', 'danger')
            return redirect(url_for('view.login'))
    return wrap
#### blueprints
bp = Blueprint('view',__name__)

#### dev models
class Event():
    title = "Lorem impsum"
    description = "Lorem ipsum dolor, sit amet consectetur adipisicing elit. Illo odit voluptas praesentium tempore quisquam nihil sint eveniet vero eligendi est!"
    date = '18:00 01.02.20'
    bg_url = "/static/img/gp-bg.jpg"

class dev_Article():
    title = "Lorem ipsum dolor sit amet consectetur, adipisicing elit."
    text = "Sunt aute ut consectetur nostrud non mollit do elit Lorem sit consequat aute proident do. Cillum fugiat nostrud dolor elit do sint esse ex quis mollit ullamco. Anim labore et consectetur id aliqua ea aliqua ipsum. Laborum ex non sunt eu consequat Lorem minim ea velit veniam sunt nostrud nulla consectetur. Velit in sint aliqua est mollit aliqua consequat culpa excepteur veniam. Ad aliqua et consequat minim consequat velit nisi ut velit elit exercitation ea magna id.\nEnim mollit exercitation ut nostrud ut do in cupidatat commodo. Labore commodo adipisicing in enim. Culpa elit consectetur laboris aute dolore culpa ex aute. Laborum ullamco incididunt ea adipisicing aute excepteur commodo tempor laborum qui nisi labore consequat duis. Ut magna mollit laborum in sint nisi commodo proident nostrud et voluptate dolore qui nostrud.\n"
    date = '18:00 01.02.20'
    bg_url = "img/news-img.jpg"
    source = "beyondf1.com"
    def __init__(self, id):
        self.id = id

events = [Event(), Event()]
dev_articles = [ dev_Article(i) for i in range(3)]


#### routes
@bp.route('/')
def home():
    articles = Article.query.all()
    return render_template('home.html', events=events, articles=articles)

@bp.route('/articles/<int:id>/')
def article(id):
    article = Article.query.get(id)
    return render_template('article.html', article=article, articles=dev_articles[:2])

@bp.route('/wiki')
def wiki():
    return render_template('wiki.html')

@bp.route('/admin/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password = sha512(bytes(password, encoding='utf-8')).digest()

        admin= Admin(username,email,password)

        db.session.add(admin)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('view.login'))
        
    return render_template('admin/register.html')

@bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = sha512(bytes(password, encoding='utf-8')).digest()

        admin = Admin.query.filter_by(username=username).first()
        if  password == admin.password:
            session['is_logged'] = True
            session['username'] = admin.username

            flash('You are logged!', 'success')
            return redirect(url_for('view.panel'))
        else:
            flash('Incorect data!', 'danger')
            return redirect(url_for('view.login'))

    return render_template('admin/login.html')

@bp.route('/admin/logout')
def logout():
    session.clear()
    flash('You are logout!', 'success')
    return redirect(url_for('view.login'))

@bp.route('/admin')
@is_loggin
def panel():
    return render_template('admin/panel.html')

## Users manipulations
@bp.route('/admin/users')
@is_loggin
def users():
    users = Admin.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/admin/users/delete/<int:id>')
@is_loggin
def user_delete(id):
    user = Admin.query.get(id)
    db.session.delete(user)
    db.session.commit()

    flash('User\'ve been deleted', 'success')
    return redirect(url_for('view.users'))


@bp.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
@is_loggin
def user_edit(id):
    user = Admin.query.get(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        password = request.form['password']
        user.password = sha512(bytes(password, encoding='utf-8')).digest()

        db.session.commit()
        session.clear()
        flash('Account updated!', 'success')
        return redirect(url_for('view.login'))

    return render_template('admin/users-edit.html', user=user)

@bp.route('/admin/users/add-new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password = sha512(bytes(password, encoding='utf-8')).digest()

        admin= Admin(username,email,password)

        db.session.add(admin)
        db.session.commit()
        flash('User created!', 'success')
        return redirect(url_for('view.users'))
        
    return render_template('admin/register.html')
## News manipulations
@bp.route('/admin/news')
@is_loggin
def news():
    news = Article.query.all()
    return render_template('admin/news.html', news=news)

@bp.route('/admin/news/delete/<int:id>')
@is_loggin
def news_delete(id):
    news = Article.query.get(id)
    db.session.delete(news)
    db.session.commit()

    flash('News\'ve been deleted', 'success')
    return redirect(url_for('view.news'))

@bp.route('/admin/news/add-new', methods=['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        title = request.form['title']
        domain = request.form['domain']
        source = request.form['source']
        bg_url = request.form['bg_url']
        text = request.form['text']

        news = Article(title,text,bg_url,domain,source)

        db.session.add(news)
        db.session.commit()
        flash('News created!', 'success')
        return redirect(url_for('view.news'))
        
    return render_template('admin/news-new.html')

@bp.route('/admin/news/edit/<int:id>', methods=['GET', 'POST'])
def edit_article(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.domain = request.form['domain']
        article.source = request.form['source']
        article.bg_url = request.form['bg_url']
        article.text = request.form['text']

        db.session.commit()

        flash('News updated!', 'success')
        return redirect(url_for('view.news'))
        
    return render_template('admin/news-edit.html', article=article)
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
    bg_url = "img/gp-bg.jpg"

class Article():
    title = "Lorem ipsum dolor sit amet consectetur, adipisicing elit."
    text = "Sunt aute ut consectetur nostrud non mollit do elit Lorem sit consequat aute proident do. Cillum fugiat nostrud dolor elit do sint esse ex quis mollit ullamco. Anim labore et consectetur id aliqua ea aliqua ipsum. Laborum ex non sunt eu consequat Lorem minim ea velit veniam sunt nostrud nulla consectetur. Velit in sint aliqua est mollit aliqua consequat culpa excepteur veniam. Ad aliqua et consequat minim consequat velit nisi ut velit elit exercitation ea magna id.\nEnim mollit exercitation ut nostrud ut do in cupidatat commodo. Labore commodo adipisicing in enim. Culpa elit consectetur laboris aute dolore culpa ex aute. Laborum ullamco incididunt ea adipisicing aute excepteur commodo tempor laborum qui nisi labore consequat duis. Ut magna mollit laborum in sint nisi commodo proident nostrud et voluptate dolore qui nostrud.\n"
    date = '18:00 01.02.20'
    bg_url = "img/news-img.jpg"
    source = "beyondf1.com"
    def __init__(self, id):
        self.id = id

events = [Event(), Event()]
articles = [ Article(i) for i in range(3)]


#### routes
@bp.route('/')
def home():
    return render_template('home.html', events=events, articles=articles)

@bp.route('/articles/<int:id>/')
def article(id):
    article = articles[id]
    return render_template('article.html', article=article, articles=articles[:2])

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

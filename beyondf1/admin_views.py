from flask import render_template, Blueprint, request, session, flash, redirect, url_for
from hashlib import sha512
from functools import wraps
from beyondf1.models import *
#### blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates/admin')
#### decorators
def is_loggin(f):
    @wraps(f)
    def wrap(*argc, **kwargs):
        if 'is_logged' in session:
            return f(*argc, **kwargs)
        else:
            flash('You need loggin!', 'danger')
            return redirect(url_for('admin.login'))
    return wrap
#### routes
@admin.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('admin.login'))
        
    return render_template('/register.html')

@admin.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('admin.panel'))
        else:
            flash('Incorect data!', 'danger')
            return redirect(url_for('admin.login'))

    return render_template('/login.html')

@admin.route('/logout')
def logout():
    session.clear()
    flash('You are logout!', 'success')
    return redirect(url_for('admin.login'))

@admin.route('/')
@is_loggin
def panel():
    return render_template('/panel.html')

## Users manipulations
@admin.route('/users')
@is_loggin
def users():
    users = Admin.query.order_by(Admin.id.desc())
    return render_template('/users.html', users=users)

@admin.route('/users/delete/<int:id>')
@is_loggin
def user_delete(id):
    user = Admin.query.get(id)
    db.session.delete(user)
    db.session.commit()

    flash('User\'ve been deleted', 'success')
    return redirect(url_for('admin.users'))


@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('admin.login'))

    return render_template('/users-edit.html', user=user)

@admin.route('/users/add-new', methods=['GET', 'POST'])
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
        return redirect(url_for('admin.users'))
        
    return render_template('/register.html')
## News manipulations
@admin.route('/news')
@is_loggin
def news():
    news = Article.query.order_by(Article.id.desc())
    return render_template('/news.html', news=news)

@admin.route('/news/delete/<int:id>')
@is_loggin
def news_delete(id):
    news = Article.query.get(id)
    db.session.delete(news)
    db.session.commit()

    flash('News\'ve been deleted', 'success')
    return redirect(url_for('admin.news'))

@admin.route('/news/add-new', methods=['GET', 'POST'])
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
        return redirect(url_for('admin.news'))
        
    return render_template('admin/news-new.html')

@admin.route('/news/edit/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('admin.news'))
        
    return render_template('/news-edit.html', article=article)
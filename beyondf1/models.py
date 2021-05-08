from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String())
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '[#] User: %r' % self.username


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    text = db.Column(db.String())
    date = db.Column(db.DateTime, default=datetime.utcnow)
    bg_url = db.Column(db.String())
    domain = db.Column(db.String(64))
    source = db.Column(db.String())

    def __init__(self,title,text,bg_url,domain,source):
        self.title = title
        self.text = text
        self.bg_url = bg_url
        self.domain = domain
        self.source = source
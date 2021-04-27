from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:238516@localhost:5432/beyondf1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] ='united'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app, name='beyondf1', template_mode='bootstrap3')

class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    short_text = db.Column(db.String(256))
    long_text = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    source = db.Column(db.String(128))
    img_url = db.Column(db.String(128))

    def __init__(self, title, short_text, long_text, source, img_url):
        self.title = title
        self.short_text = short_text
        self.long_text = long_text
        self.source = source
        self.img_url = img_url

    def __repr__(self):
        return f'<News: {self.id}>'


@app.route('/')
def home():
    return render_template('home.html')


admin.add_view(ModelView(Article,db.session))

if __name__ == '__main__':
    app.run()
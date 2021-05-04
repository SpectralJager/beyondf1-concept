import requests
from datetime import datetime
from bs4 import BeautifulSoup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True, nullable=False)
    text = db.Column(db.String(), nullable=False)
    domain = db.Column(db.String(256), nullable=False)
    source = db.Column(db.String(512), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    def __init__(self, title, text, domain, source):
        self.title = title
        self.text = text
        self.domain = domain
        self.source = source

    

class NewsCrawler():
    headers ={
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    }

    formula1 = {   
        'domain': 'https://www.formula1.com/',
        'url': "en/latest/all.html",
        'params': {
            'block_class': 'f1-latest-listing--grid-item',
            'tag_class': 'misc--tag',
            'article_link_name': 'a',
            'title': 'f1-article--title',
            'article_content': 'f1-article--rich-text',
        },
    }
    planetf1 = {   
        'name': 'Planetf1',
        'domain': 'https://www.planetf1.com/',
        'url': "news/",
        'params': {
            'block_class': 'articleList__item',
            'tag_class': 'bypass',
            'article_link_name': 'a',
            'title': 'article__header',
            'article_content': 'ciam-article-pf1',
        },
    }
    def isExist(self, t):
        if News.query.filter_by(title=t).first():
            return 1
        else:
            return 0

    def formula1Check(self):
        print('[#]start checking updates on formula1.com')
        # create request and get page
        resp = requests.get(self.formula1['domain']+self.formula1['url'], headers=self.headers)
        # create parser
        parser = BeautifulSoup(resp.content, 'html5lib')
        params = self.formula1['params']
        # find all articles
        articles = parser.find_all(class_=params['block_class'])
        for article in articles:
            #find news
            if article.find(class_=params['tag_class']).get_text(strip=True) != 'News':
                continue
            else:
                print('[#] Found news')
                #get news href
                href = article.find(params['article_link_name'])['href']
                # get full article
                url = self.formula1['domain'] + href
                resp = requests.get(url, headers=self.headers)
                article = BeautifulSoup(resp.content, 'html5lib')
                # get title
                title = article.find(class_=params['title']).get_text(strip=True)
                print(f'[#] Title: \'{title}\'')
                print('[#] Checking, if it in datebase...')
                # check if news exist
                if self.isExist(title):
                    print(f'[#] News: \'{title}\' is existing..')
                    print('[#] Updates no neaded. Bye')
                    return 1
                else:
                    # get text
                    print('[#] Download text...')
                    text = article.find_all(class_=params['article_content'])
                    text = '\n'.join([ i.get_text(strip=True) for i in text ])
                    print('[#] Create news model...')
                    news = News(title, text, self.formula1['domain'], url)
                    print('[#] Add to datebase...')
                    db.session.add(news)
                    db.session.commit()
                    print('[#] Done. Check next...')
        print('[#] All news updated...')

if __name__ == '__main__':
    app.run()
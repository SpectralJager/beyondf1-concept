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
            'title': 'h1',
            'article_content': 'f1-article--rich-text',
        },
    }
    planetf1 = {   
        'name': 'Planetf1',
        'domain': 'https://www.planetf1.com/',
        'url': "news/",
        'params': {
            'hero_class': 'hero',
            'hero_items': 'figure',
            'list_item_class': 'articleList__item',
            'article_link_name': 'a',
            'title': 'h1',
            'article_content': 'ciam-article-pf1',
        },
    }
    def updateNews(self):
        print('[#] Start check for update all news bases...')
        self.planetf1Check()
        print('[#] Next... \n')
        self.formula1Check()
        print('[#] DONE.')

    def isExist(self, t):
        if News.query.filter_by(title=t).first():
            return 1
        else:
            return 0

    def planetf1Check(self):
        print('[#]start checking updates on planetf1.com')
        # create request and get page
        resp = requests.get(self.planetf1['domain']+self.planetf1['url'], headers=self.headers)
        # create parser
        parser = BeautifulSoup(resp.content, 'html5lib')
        params = self.planetf1['params']
        # find all articles
        hero = parser.find(class_=params['hero_class'])
        articles = hero.find_all(params['hero_items'])
        for article in articles:
            #find news
            print('[#] Found news')
            #get news href
            href = article.find(params['article_link_name'])['href']
            # get full article
            article_resp = requests.get(href, headers=self.headers)
            article_parser = BeautifulSoup(article_resp.content, 'html5lib')
            # get title
            title = article_parser.find(params['title']).get_text(strip=True)
            print(f'[#] Title: \'{title}\'')
            print('[#] Checking, if it in datebase...')
            # check if news exist
            if self.isExist(title):
                print(f'[#] News: \'{title}\' is existing..')
                break
            else:
                # get text
                print('[#] Download text...')
                text = article_parser.find(class_=params['article_content']).get_text(strip=True)
                print('[#] Create news model...')
                news = News(title, text, self.planetf1['domain'], href)
                print('[#] Add to datebase...')
                db.session.add(news)
                db.session.commit()
                print('[#] Done. Check next...')

        articles = parser.find_all(class_=params['list_item_class'])
        for article in articles:
            #find news
            print('[#] Found news')
            #get news href
            href = article.find(params['article_link_name'])['href']
            # get full article
            article_resp = requests.get(href, headers=self.headers)
            article_parser = BeautifulSoup(article_resp.content, 'html5lib')
            # get title
            title = article_parser.find(params['title']).get_text(strip=True)
            print(f'[#] Title: \'{title}\'')
            print('[#] Checking, if it in datebase...')
            # check if news exist
            if self.isExist(title):
                print(f'[#] News: \'{title}\' is existing..')
                break
            else:
                # get text
                print('[#] Download text...')
                text = article_parser.find(class_=params['article_content']).get_text(strip=True)
                print('[#] Create news model...')
                news = News(title, text, self.planetf1['domain'], href)
                print('[#] Add to datebase...')
                db.session.add(news)
                db.session.commit()
                print('[#] Done. Check next...')
        print('[#] All news updated...')

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
            if article.find(class_=params['tag_class']).get_text(strip=True) != 'News' and article.find(class_=params['tag_class']).get_text(strip=True) != 'Breaking News':
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
                title = article.find(params['title']).get_text(strip=True)
                print(f'[#] Title: \'{title}\'')
                print('[#] Checking, if it in datebase...')
                # check if news exist
                if self.isExist(title):
                    print(f'[#] News: \'{title}\' is existing..')
                    break
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


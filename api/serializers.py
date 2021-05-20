from rest_framework import serializers
from .models import Article, Subscribers

class ArticleSerializer(serializers.ModelSerializer):
    published_date = serializers.DateTimeField(format="%Y-%m-%d %H:%m")
    class Meta:
        model = Article
        fields = ('id','title','bg_url','published_date','text')

class SubscribersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribers
        fields = ('id','email')
from rest_framework import serializers, viewsets
from .models import Article, Subscribers
from .serializers import ArticleSerializer, SubscribersSerializer
# Create your views here.

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-published_date')
    serializer_class = ArticleSerializer
    http_method_names = ['get']

class SubscribersViewSet(viewsets.ModelViewSet):
    queryset = Subscribers.objects.all()
    serializer_class = SubscribersSerializer
    http_method_names = ['post']
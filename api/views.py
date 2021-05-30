from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Article, Subscribers
from .serializers import ArticleSerializer, SubscribersSerializer


#pagination class
class HomePagePagination(PageNumberPagination):
    page_size = 8
    page_query_param = "page_size"
    max_page_size = 80

# Create your views here.
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-published_date')
    serializer_class = ArticleSerializer
    pagination_class = HomePagePagination
    http_method_names = ['get']

class SubscribersViewSet(viewsets.ModelViewSet):
    queryset = Subscribers.objects.all()
    serializer_class = SubscribersSerializer
    http_method_names = ['post']
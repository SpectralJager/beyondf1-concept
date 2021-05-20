from rest_framework import routers, urlpatterns
from .views import ArticleViewSet, SubscribersViewSet

router = routers.DefaultRouter()
router.register(r'article', ArticleViewSet)
router.register(r'subscribers', SubscribersViewSet)

urlpatterns = router.urls
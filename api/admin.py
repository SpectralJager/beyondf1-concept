from django.contrib import admin
from .models import Article, Subscribers
# Register your models here.
admin.site.register([Subscribers,Article])

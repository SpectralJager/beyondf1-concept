from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Article(models.Model):
    title = models.CharField('Title', max_length=256, unique=True, null=False)
    bg_url = models.URLField('Background URL', null=False)
    published_date = models.DateTimeField('Published date', auto_now_add=True)
    text = RichTextField('Text', null=False)

    def __str__(self) -> str:
        return '[#] Article: %r' % (self.title[:20])

class Subscribers(models.Model):
    email = models.EmailField('Email', unique=True, null=False)

    def __repr__(self) -> str:
        return '[#] Email: %r' % self.email

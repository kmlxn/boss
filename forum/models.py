import datetime

from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def topic_count(self):
        return self.topic_set.count()


class Topic(models.Model):
    category = models.ForeignKey(Category, null=True)
    number = models.IntegerField()
    name = models.CharField(max_length=255)
    text = models.TextField()
    pub_date = models.DateTimeField('date published')
    publishers_ip = models.CharField(max_length=100)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    image = models.FileField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return self.text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Comment(models.Model):
    topic = models.ForeignKey(Topic)
    number = models.IntegerField()
    text = models.TextField()
    publishers_ip = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    image = models.FileField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return self.text
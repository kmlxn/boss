import datetime
from math import log

from django.db import models
from django.utils import timezone



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()


    def __str__(self):
        return self.title


    def topic_count(self):
        return self.topic_set.count()



class Topic(models.Model):
    category = models.ForeignKey(Category, null=True)
    number = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    text = models.TextField()
    pub_date = models.DateTimeField('date published')
    publishers_ip = models.CharField(max_length=100)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='images', null=True, blank=True)


    def __str__(self):
        return self.name


    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


    def hot(self):
        """Reddit ranking algorithm. Original version -
        https://github.com/reddit/reddit/blob/master/r2/r2/lib/db/_sorts.pyx"""
        s = self._score(self.upvotes, self.downvotes)
        order = log(max(abs(s), 1), 10)
        sign = 1 if s > 0 else -1 if s < 0 else 0
        seconds = self._epoch_seconds(self.pub_date) - 1134028003
        return round(sign * order + seconds / 45000, 7)


    def _epoch_seconds(self, date):
        epoch = timezone.make_aware(datetime.datetime(1970, 1, 1), timezone.get_default_timezone())
        td = date - epoch
        return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)


    def _score(self, ups, downs):
        return ups - downs


    def controversy(self):
        """Reddit controversy algorithm. Original version -
        https://github.com/reddit/reddit/blob/master/r2/r2/lib/db/_sorts.pyx"""
        if self.downvotes <= 0 or self.upvotes <= 0:
            return 0

        magnitude = self.upvotes + self.downvotes

        if self.upvotes > self.downvotes:
            balance = float(self.downvotes) / self.upvotes
        else:
            balance = float(self.upvotes) / self.downvotes

        return magnitude ** balance



class Comment(models.Model):
    topic = models.ForeignKey(Topic)
    number = models.IntegerField()
    text = models.TextField()
    publishers_ip = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='images', null=True, blank=True)


    def __str__(self):
        return self.text

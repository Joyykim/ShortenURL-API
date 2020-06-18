import string
import time

from django.db import models

words = string.ascii_letters + string.digits


class Link(models.Model):
    realURL = models.URLField()
    _shortURL = models.CharField(max_length=200)
    hits = models.IntegerField(default=0)
    owner = models.ForeignKey('users.User', related_name='links', on_delete=models.CASCADE, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.shortURL = self.long_to_short()
        super().save(force_insert, force_update, using, update_fields)

    @property
    def shortURL(self):
        return f"http://127.0.0.1:8000/api/link/{self._shortURL}"

    @shortURL.setter
    def shortURL(self, val):
        self._shortURL = val

    def long_to_short(self):
        result = 0
        for s in self.realURL:
            result += ord(s)
        result += int(time.time() * 1000)
        return self.base62(result)

    def base62(self, index):
        result = ""
        while (index % 62) > 0 or result == "":
            index, i = divmod(index, 62)
            result += words[i]
        return result


class PollManager(models.Manager):

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class OpinionPoll(models.Model):
    question = models.CharField(max_length=200)
    poll_date = models.DateField()
    objects = PollManager()


class Response(models.Model):
    poll = models.ForeignKey(OpinionPoll, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=50)
    response = models.TextField()

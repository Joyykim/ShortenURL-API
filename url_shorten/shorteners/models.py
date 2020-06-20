import string
import time
import uuid

import psycopg2
from django.db import models, IntegrityError

words = string.ascii_letters + string.digits


class Link(models.Model):
    realURL = models.URLField()
    _shortURL = models.CharField(max_length=200, unique=True)
    hits = models.IntegerField(default=0)
    owner = models.ForeignKey('users.User', related_name='links', on_delete=models.CASCADE, null=True)
    # custom = models.CharField(max_length=20, null=True)
    is_custom = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.is_custom:
            self._shortURL = self.make_short_base62()
        super().save(force_insert, force_update, using, update_fields)

    @property
    def shortURL(self):
        return f"http://127.0.0.1:8000/api/link/{self._shortURL}"

    def make_short_uuid(self):
        u = uuid.uuid4()[:6]
        print(u)
        pass

    def make_short_base62(self):
        result = 0
        for s in self.realURL:
            result += ord(s)
        result = str(result) + str(int(time.time() * 1000))
        return self.base62(int(result))

    def base62(self, index):
        result = ""
        while (index % 62) > 0 or result == "":
            index, i = divmod(index, 62)
            result += words[i]
        return result

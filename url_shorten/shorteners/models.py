import string
import time
from uuid import uuid4

import psycopg2
from django.db import models, IntegrityError

words = string.ascii_letters + string.digits


class Link(models.Model):
    realURL = models.URLField()
    _shortURL = models.CharField(max_length=200, unique=True)
    hits = models.IntegerField(default=0)
    owner = models.ForeignKey('users.User', related_name='links', on_delete=models.CASCADE, null=True)
    is_custom = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if (not self.hits) and (not self.is_custom):
            self.shortURL = self.make_short_uuid()
        super().save(force_insert, force_update, using, update_fields)

    @property
    def shortURL(self):
        return f"http://127.0.0.1:8000/api/link/{self._shortURL}"

    @shortURL.setter
    def shortURL(self, val):
        self._shortURL = val

    def make_short_uuid(self):
        """20번 모두 uuid 중복 발생 시"""
        for i in range(20):
            u = uuid4().hex[:6]
            if not Link.objects.filter(_shortURL=u).exists():
                return u

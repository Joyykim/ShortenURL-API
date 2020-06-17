import string
import time

from django.db import models

words = string.ascii_letters + string.digits


class Link(models.Model):
    realURL = models.URLField()
    _shortURL = models.CharField(max_length=200)
    hits = models.IntegerField(default=0)
    owner = models.ForeignKey('users.User', related_name='links', on_delete=models.CASCADE)

    # owner = models.ForeignKey('users.User', related_name='links', on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.shortURL = self.long_to_short()
        super().save(force_insert, force_update, using, update_fields)

    @property
    def shortURL(self):
        # short_url = f"{request.scheme}://{request.get_host()}/api/link/{self._shortURL}"
        return f"http://127.0.0.1:8000/api/link/{self._shortURL}"

    @shortURL.setter
    def shortURL(self, val):
        self._shortURL = val

    def long_to_short(self):
        result = 0
        for s in self.realURL:
            result += ord(s)
        for s in self.owner.username:
            result += ord(s)
        result += int(time.time())
        return self.base62(result)

    def base62(self, index):
        result = ""
        while (index % 62) > 0 or result == "":
            index, i = divmod(index, 62)
            result += words[i]
        return result

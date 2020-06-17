from django.db import models
import time
import string

words = string.ascii_letters + string.digits


class Link(models.Model):
    realURL = models.URLField()
    _shortURL = models.CharField(max_length=200)
    hits = models.IntegerField(default=0)
    owner = models.ForeignKey('users.User', related_name='links', on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        a = int(time.time())
        print(a)
        super().save(force_insert, force_update, using, update_fields)

    # def get_shortURL(self, obj):
    #     # short_url = f"http:8000//127.0.0.1/api/link/{obj.shortURL}"
    #     request = self.context['request']
    #     short_url = f"{request.scheme}://{request.get_host()}/api/link/{obj.shortURL}"
    #     return short_url

    @property
    def shortURL(self):
        request = self
        # short_url = f"{request.scheme}://{request.get_host()}/api/link/{self._shortURL}"
        short_url = f"http://127.0.0.1/api/link/{self._shortURL}"
        return short_url

    def long_to_short(self):
        result = 0
        for s in self.realURL:
            result += ord(s)
        result += int(time.time())
        return result

    def base62(self, index):
        result = ""
        while (index % 62) > 0 or result == "":
            index, i = divmod(index, 62)
            result += words[i]
        return result

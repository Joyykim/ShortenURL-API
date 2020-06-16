from django.db import models


class Link(models.Model):
    realURL = models.URLField()
    shortURL = models.URLField()
    hits = models.IntegerField(default=0)

    def __repr__(self):
        return "<Link (Hits %s): %s>" % (self.hits, self.realURL)

# from shorteners.models import Link
# # Link.objects.create(realURL='https://www.naver.com/')
# # link = Link.objects.get(pk=1)
# # short = link.get_short_id()

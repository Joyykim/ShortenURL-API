from django.db import models


class Link(models.Model):
    realURL = models.URLField()
    shortURL = models.CharField(max_length=200)
    hits = models.IntegerField(default=0)

    def __repr__(self):
        return f"<Link (Hits {self.hits}): {self.realURL}>"

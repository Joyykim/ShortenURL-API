from django.db import models
import string

_char_map = string.ascii_letters + string.digits


def index_to_char(sequence):
    return "".join([_char_map[x] for x in sequence])


class Link(models.Model):
    realURL = models.URLField()
    ShortenURL = models.URLField()
    hits = models.IntegerField(default=0)

    def __repr__(self):
        return "<Link (Hits %s): %s>" % (self.hits, self.realURL)

    def get_short_id(self):
        _id = self.id
        digits = []
        while _id > 0:
            rem = _id % 62
            digits.append(rem)
            _id /= 62
        digits.reverse()
        return index_to_char(digits)

    @classmethod
    def decode_id(cls, s):
        i = 0
        for c in s:
            i = i * 64 + _char_map.index(c)
        return i

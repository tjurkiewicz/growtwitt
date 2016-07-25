
import django.db.models


class FollowersCacheEntry(django.db.models.Model):
    uuid4 = django.db.models.CharField(max_length=32)
    screen_name = django.db.models.CharField(max_length=128)
    following = django.db.models.PositiveIntegerField()

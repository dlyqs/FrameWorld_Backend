from django.db import models
from django.contrib.auth.models import User


class Entry(models.Model):
    TYPE_CHOICES = [('Video', 'Audio')]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Video')
    title = models.CharField(max_length=255)
    version = models.CharField(max_length=100)
    length = models.FloatField()
    x_frame_size = models.FloatField()
    y_frame_size = models.FloatField()
    douban_url = models.URLField(blank=True, null=True)
    imdb_url = models.URLField(blank=True, null=True)
    cover_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class GlobalComment(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    time = models.DateTimeField()
    content = models.TextField()
    parentID = models.TextField(blank=True, null=True)
    replies = models.TextField(blank=True, null=True)
    popularity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class FrameComment(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    timestamp = models.FloatField()
    content = models.TextField()
    replies = models.TextField(blank=True, null=True)
    popularity = models.IntegerField()
    x_position = models.CharField(max_length=10, blank=True, null=True)
    y_position = models.CharField(max_length=10, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Subtitle(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    timestamp = models.FloatField()
    content = models.TextField()
    duration = models.FloatField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class LikeRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(GlobalComment, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)  # True for liked, False for no like

    class Meta:
        unique_together = ('user', 'comment')
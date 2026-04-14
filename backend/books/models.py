from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    rating = models.FloatField(default=0)
    book_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

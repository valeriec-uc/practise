from django.db import models

# Create your models here.
from django.db import models


class Author(models.Model):
    # ...
    author_text = models.CharField(max_length=200)
    DateOfBirth = models.CharField(max_length=200)
    author_desc = models.TextField()


    def __str__(self):
        return self.author_text


class Tag(models.Model):
    # ...
    tag_name = models.CharField(max_length=200 , unique=True)

    def __str__(self):
        return self.tag_name


class Quotes(models.Model):
    # ...
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quotes_text = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.quotes_text


class Link(models.Model):
    # ...
    quotes = models.ForeignKey(Quotes, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.author

    class Meta:
        unique_together = ('quotes_id', 'tag_id',)



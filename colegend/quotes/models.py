from django.conf import settings
from django.db import models

__author__ = 'eraldo'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Quote(models.Model):
    """A motivational text quote."""

    name = models.CharField(max_length=100, unique=True)
    text = models.TextField(blank=True)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
    provider = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name

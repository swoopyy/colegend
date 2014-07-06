from django.db import models

__author__ = 'eraldo'


class StatusFiltersMixin:
    def open(self):
        return self.filter(status__type=Status.OPEN)

    def closed(self):
        return self.filter(status__type=Status.CLOSED)

    def status(self, status):
        """
        Filters the QuerySet based on a given status.

        :param status: status, status name or status type (open|closed) to filter on
        :return: filtered QuerySet
        """
        if status == "open":
            return self.open()
        elif status == "closed":
            return self.closed()
        return self.filter(status__name=status)


class StatusManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

    def open(self):
        return self.filter(type=Status.OPEN)

    def closed(self):
        return self.filter(type=Status.CLOSED)


class Status(models.Model):
    """
    Django model representing a processing state.
    """
    name = models.CharField(max_length=50, unique=True)

    OPEN = "open"
    CLOSED = "closed"
    DEFAULT = OPEN
    TYPES = (
        (OPEN, "open"),
        (CLOSED, "closed"),
    )
    type = models.CharField(default=DEFAULT, max_length=50, choices=TYPES)
    order = models.PositiveIntegerField(unique=True)
    DEFAULT_PK = 1

    objects = StatusManager()

    class Meta:
        verbose_name_plural = "Status"
        ordering = ['order']

    def __str__(self):
        return self.name

    def natural_key(self):
        return [self.name]

    def open(self):
        return self.type == self.OPEN

    def closed(self):
        return self.type == self.CLOSED


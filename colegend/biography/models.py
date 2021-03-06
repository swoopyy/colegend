from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext as _
from colegend.core.models import SingleOwnedBase, TimeStampedBase


class Biography(SingleOwnedBase, TimeStampedBase):
    """
    A django model representing the legend's biography.
    """
    text = models.TextField(blank=True)

    def __str__(self):
        return _("{}'s biography").format(self.owner)

    @staticmethod
    def get_absolute_url():
        return reverse('biography:update')

from django.utils.translation import ugettext_lazy as _
from django.db import models

from colegend.core.fields import MarkdownField
from colegend.core.models import AutoOwnedBase, AutoUrlsMixin, OwnedQuerySet


class JournalQuerySet(OwnedQuerySet):
    pass


class Journal(AutoUrlsMixin, AutoOwnedBase):
    """
    A django model representing a user's journal.
    """

    spellchecker = models.BooleanField(default=False)
    day_template = MarkdownField(blank=True)
    week_template = MarkdownField(blank=True)
    month_template = MarkdownField(blank=True)

    objects = JournalQuerySet.as_manager()

    class Meta:
        verbose_name = _('Journal')
        verbose_name_plural = _('Journals')

    def __str__(self):
        return "{}'s journal".format(self.owner)

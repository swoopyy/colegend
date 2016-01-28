from annoying.fields import AutoOneToOneField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


class TimeStampedBase(models.Model):
    """
    Adds created and last modified fields to a model.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OwnedCheckMixin(object):
    """
    Adds the ability to check ownership to a model.
    """

    def owned_by(self, user):
        if user == self.owner:
            return True
        else:
            return False


class OwnedBase(OwnedCheckMixin, models.Model):
    """
    Adds a owner (user) field to the model. 1-*
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True


class SingleOwnedBase(OwnedCheckMixin, models.Model):
    """
    Adds a owner (user) field to the model. 1-1
    """
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True


class AutoOwnedBase(OwnedCheckMixin, models.Model):
    """
    Adds a owner (user) field to the model. 1-1
    The inheriting model is automatically created on retrieval.
    """
    owner = AutoOneToOneField(settings.AUTH_USER_MODEL, primary_key=True)

    class Meta:
        abstract = True


class OwnedQuerySet(models.QuerySet):
    """
    Enable the queryset to be filtered by owning users.
    """

    def owned_by(self, user):
        return self.filter(owner=user)


class AutoUrlsMixin(object):
    """
    A mixin that automatically adds the CRUD urls to the model.
    """

    @property
    def index_url(self):
        app = self._meta.app_label
        url = '{}:index'.format(app)
        return reverse(url)

    @property
    def list_url(self):
        app = self._meta.app_label
        url = '{}:list'.format(app)
        return reverse(url)

    @property
    def create_url(self):
        app = self._meta.app_label
        url = '{}:create'.format(app)
        return reverse(url)

    @property
    def detail_url(self):
        app = self._meta.app_label
        url = '{}:detail'.format(app)
        return reverse(url, kwargs={'pk': self.pk})

    @property
    def update_url(self):
        app = self._meta.app_label
        url = '{}:update'.format(app)
        return reverse(url, kwargs={'pk': self.pk})

    @property
    def delete_url(self):
        app = self._meta.app_label
        url = '{}:delete'.format(app)
        return reverse(url, kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return self.detail_url
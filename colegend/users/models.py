# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import hashlib
from enum import Enum
from urllib.parse import quote_plus

from allauth.account.signals import user_signed_up
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, UserManager as AuthUserManager
from django.core.mail import EmailMessage
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django_slack import slack_message
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.fields import ThumbnailerImageField
from phonenumber_field.modelfields import PhoneNumberField

from colegend.chat.tasks import send_chat_message, Channel
from colegend.checkpoints.models import Checkpoint
from colegend.community.models import Duo, Clan, Tribe
from colegend.core.fields import MarkdownField
from colegend.core.models import TimeStampedBase, OwnedBase
from colegend.core.utils.media_paths import UploadToOwnedDirectory
from colegend.outcomes.models import Step
from colegend.roles.models import Role

SYSTEM_USER_USERNAME = 'coLegend'


class ImageSize(Enum):
    MINI = 'MINI'
    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'
    LARGE = 'LARGE'


class UserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def premium(self):
        return self.filter(is_premium=True)


class UserManager(AuthUserManager.from_queryset(UserQuerySet)):
    pass


class UserCheckpoint(OwnedBase, TimeStampedBase):
    checkpoint = models.ForeignKey(
        to=Checkpoint, on_delete=models.CASCADE
    )

    class Meta:
        default_related_name = 'user_checkpoints'
        unique_together = ['owner', 'checkpoint']
        verbose_name = _("User Checkpoint")
        verbose_name_plural = _("User Checkpoints")

    def __str__(self):
        return f'[{self.owner}] {self.checkpoint}'


class User(AbstractUser):
    """
    A django model representing a coLegend user/member called 'Legend'.
    """
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
        help_text=_("Your full name"),
    )
    # personal and contact data
    MALE = 'M'
    FEMALE = 'F'
    NEUTRAL = 'N'
    GENDER_CHOICES = (
        (MALE, _('male')),
        (FEMALE, _('female')),
        (NEUTRAL, _('neutral')),
    )
    gender = models.CharField(
        verbose_name=_('gender'),
        max_length=1,
        choices=GENDER_CHOICES,
        default=NEUTRAL
    )

    birthday = models.DateField(
        verbose_name=_('birthday'),
        null=True, blank=True,
    )

    address = models.TextField(
        verbose_name=_('address'),
        blank=True
    )

    @property
    def city(self):
        address = self.address
        city = ''
        if address:
            parts = address.splitlines()
            if len(parts) >= 2:
                city = parts[1]
        return city

    phone = PhoneNumberField(
        verbose_name=_('phone'),
        blank=True,
        help_text=_('International format: e.g "+4917612345678"')
    )

    occupation = models.CharField(
        verbose_name=_('occupation(s)'),
        max_length=255,
        blank=True
    )

    avatar = ThumbnailerImageField(
        verbose_name=_('avatar'),
        upload_to=UploadToOwnedDirectory('avatars'),
        resize_source=dict(size=(400, 400)),
        blank=True
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        blank=True
    )

    purpose = models.CharField(
        verbose_name=_("legend purpose"),
        max_length=255,
        help_text=_("I am a legend, <what you are doing or being> as <the role you are doing it as>."),
        default=_("I am a legend, defining my legend purpose as a member of coLegend.")
    )

    notes = MarkdownField(
        verbose_name=_("notes"),
        help_text=_("Staff notes."),
        blank=True
    )

    def add_note(self, note):
        if note:
            self.notes += '[{timestamp}] {note}\n'.format(
                timestamp=timezone.localtime(timezone.now()).isoformat(),
                note=note
            )
            self.save()

    def get_avatar(self, size=ImageSize.MEDIUM.value):
        # Issue with thumbnail creation:
        #  https://github.com/SmileyChris/easy-thumbnails/issues/499
        #  https://github.com/SmileyChris/easy-thumbnails/issues/503

        try:
            return self.avatar[size]
        except InvalidImageFormatError:
            if self.avatar:
                return self.avatar
        return self.avatar or self.get_avatar_fallback(size)

    def get_avatar_fallback(self, size=ImageSize.MEDIUM.value):
        email_md5 = hashlib.md5(self.email.encode('utf-8')).hexdigest() if self.email else ''
        name = quote_plus(self.name) if self.name else 'Anonymous'
        return 'https://www.gravatar.com/avatar/{email_md5}?s={size}&d=https%3A%2F%2Fui-avatars.com%2Fapi%2F/{name}/{size}/{bg_color}/{fg_color}'.format(
            email_md5=email_md5,
            name=name,
            size=settings.THUMBNAIL_ALIASES.get('')[size]['size'][0],
            bg_color='A5D6A7',
            fg_color='fff',
        )

    roles = models.ManyToManyField(
        Role,
        blank=True,
    )

    checkpoints = models.ManyToManyField(
        Checkpoint,
        through=UserCheckpoint,
        blank=True,
    )

    balance = models.SmallIntegerField(
        verbose_name=_('balance'),
        default=0,
        help_text=_('¤')
    )

    is_premium = models.BooleanField(
        verbose_name=_('premium'),
        default=False,
        help_text=_(
            'Designates whether this user has access to premium content.'
        ),
    )

    status = models.TextField(
        verbose_name=_("status"),
        blank=True,
    )

    chat_id = models.CharField(
        verbose_name=_("chat id"),
        max_length=255,
        null=True, blank=True,
        unique=True,
    )

    duo = models.ForeignKey(
        verbose_name=_('duo'),
        to=Duo,
        related_name='members',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    clan = models.ForeignKey(
        verbose_name=_('clan'),
        to=Clan,
        related_name='members',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    tribe = models.ForeignKey(
        verbose_name=_('tribe'),
        to=Tribe,
        related_name='members',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    mentor = models.ForeignKey(
        verbose_name=_('mentor'),
        to='self',
        related_name='mentees',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    def has_checkpoint(self, name):
        return self.checkpoints.contains_name(name)

    def add_checkpoint(self, name):
        # Get the checkpoint.
        checkpoint, created = Checkpoint.objects.get_or_create(name=name)
        # Own it if not owned already.
        UserCheckpoint.objects.get_or_create(owner=self, checkpoint=checkpoint)
        return checkpoint

    def has_role(self, name):
        return self.is_superuser or self.roles.contains_name(name)

    def add_role(self, name):
        role, created = Role.objects.get_or_create(name=name)
        self.roles.add(role)
        return role

    @property
    def legend_days(self):
        date_joined = self.date_joined
        now = timezone.now()
        days = (now - date_joined).days
        return days

    @property
    def steps(self):
        steps = Step.objects.filter(outcome__owner=self)
        return steps

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('legends:detail', kwargs={'username': self.username})

    objects = UserManager()

    class Meta:
        verbose_name = 'legend'
        verbose_name_plural = 'legends'
        default_related_name = 'users'
        ordering = ['username']

    registration_country = models.CharField(max_length=255, blank=True)

    def get_pronoun(self, kind='subject'):
        gender = self.gender or self.NEUTRAL

        SUBJECT = 'subject'
        OBJECT = 'object'
        POSSESSIVE_ADJECTIVE = 'possessive adjective'
        POSSESSIVE_PRONOUN = 'possessive pronoun'
        REFLEXIVE_PRONOUN = 'reflexive pronoun'

        gender_pronouns = {
            self.MALE: {
                SUBJECT: 'he',
                OBJECT: 'him',
                POSSESSIVE_ADJECTIVE: 'his',
                POSSESSIVE_PRONOUN: 'his',
                REFLEXIVE_PRONOUN: 'himself',
            },
            self.FEMALE: {
                'subject': 'she',
                'object': 'her',
                'possessive adjective': 'her',
                'possessive pronoun': 'hers',
                'reflexive pronoun': 'herself',
            },
            self.NEUTRAL: {
                'subject': 'it',
                'object': 'it',
                'possessive adjective': 'its',
                'possessive pronoun': '',
                'reflexive pronoun': 'itself',
            },
        }
        return gender_pronouns.get(gender).get(kind)

    def contact(self, sender, subject=None, message=''):
        if not sender:
            sender = User.objects.get_or_create(username=SYSTEM_USER_USERNAME)
        if not subject:
            subject = 'Message from {name}'.format(name=sender)
        if self.email:
            email = EmailMessage(subject=subject, body=message, to=[self.email], reply_to=[sender.email])
            email.send()


@receiver(user_signed_up)
def new_user_notification(request, user, **kwargs):
    """
    Sends an email notification and a chat message upon successful user signup.

    The Email is sent to the site managers.
    The chat message is sent to the default slack channel from the project settings.
    :param request:
    :param user:
    :param kwargs:
    :return:
    """
    # manager_group, created_group = Group.objects.get_or_create(name="managers")
    # managers = [user.email for user in manager_group.user_set.all()]
    # TODO: Switch to managers group as soon as it is stable
    managers = ['connect@coLegend.org']
    reply_emails = [user.email]
    subject = f"New user: {user.username}"
    message = f"Hurray! {user.name} has joined the circle of legends."

    email = EmailMessage(subject=subject, body=message, to=managers, reply_to=reply_emails)
    email.send()

    embed = {
        'author': {
            'name': user.name,
            'icon_url': user.get_avatar()
        },
        'description': f'I want us to make {user.name} feel welcome here. ;)'
    }
    send_chat_message.delay(message, embeds=[embed], channel=Channel.COMMUNITY.value)

    slack_message('slack/message.slack', {'message': '@channel: {}'.format(message), }, fail_silently=False)

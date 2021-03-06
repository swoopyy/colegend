from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from ordered_model.admin import OrderedModelAdmin

from .models import Lead, Status, Tag


@admin.register(Status)
class StatusAdmin(OrderedModelAdmin):
    list_display = ['name', 'move_up_down_links']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'status', 'next_contact'),
            )
        }),
        (_('Progress'), {
            'fields': (
                ('history', 'notes'),
                'tags',
                ('first_contact', 'last_contact')
            )
        }),
        (_('Contact info'), {
            'fields': (
                'url', ('email', 'phone'),
                ('country', 'address')
            )
        }),
        (_('Personal info'), {
            'fields': (
                ('gender', 'birthday'),
            )
        }),
        (_('Meta info'), {
            'fields': (
                ('creator', 'created', 'modified')
            )
        }),
    )
    readonly_fields = ['modified', 'creator']
    list_display = ['name', 'status', 'next_contact', 'get_contact']
    list_editable = ['status', 'next_contact']
    list_filter = ['status', 'tags', 'next_contact', 'last_contact', 'birthday', 'country', 'gender', 'creator']
    filter_horizontal = ['tags']
    search_fields = ['name', 'history', 'notes']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def get_contact(self, obj):
        if obj.email:
            return format_html(
                '<a href="mailto:{email}" target="_blank">{email}</a>',
                email=obj.email,
            )
        if obj.url:
            return format_html(
                '<a href="{url}" target="_blank">{url}</a>',
                url=obj.url,
            )
        if obj.phone:
            return format_html(
                '<a href="tel:{phone}" target="_blank">{phone}</a>',
                phone=obj.phone,
            )

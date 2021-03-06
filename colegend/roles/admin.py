from django.contrib import admin
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from .models import Role


class RoleUserInline(admin.TabularInline):
    verbose_name = _('User')
    verbose_name_plural = _('Users')
    model = Role.users.through
    extra = 0
    show_change_link = True


class RoleInline(admin.TabularInline):
    model = Role
    fields = ['name', 'nickname', 'item', 'kind', 'circle']
    extra = 0
    show_change_link = True


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'nickname', 'item', 'users_count', 'kind', 'has_icon', 'circle']
    list_filter = ['kind', 'circle', 'users']
    search_fields = ['name', 'nickname', 'item', 'purpose', 'strategy', 'powers', 'services', 'policies', 'history',
                     'notes', 'checklists', 'metrics']
    inlines = [RoleUserInline, RoleInline]

    def get_queryset(self, request):
        """
        Annotating the queryset to prevent extra queries for many to many counts.
        :param request:
        :return: Annotated queryset
        """
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _users_count=Count('users', distinct=True),
        )
        return queryset

    def users_count(self, obj):
        return obj._users_count

    users_count.short_description = 'Users'
    users_count.admin_order_field = '_users_count'

    def has_icon(self, obj):
        return bool(obj.icon)

    has_icon.boolean = True

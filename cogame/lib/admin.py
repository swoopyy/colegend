from django.core.urlresolvers import reverse

__author__ = 'eraldo'


class InlineMixin:
    def change_link(instance):
        if not instance.id:
            return "(save and then edit)"
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.module_name),  args=[instance.id])
        return u'<a href="{u}">Edit</a>'.format(u=url)
    change_link.allow_tags = True
    change_link.short_description = 'edit?'   # omit column header

    from django.forms import TextInput, Textarea
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})},
    }

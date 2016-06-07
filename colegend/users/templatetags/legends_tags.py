from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from colegend.core.templatetags.core_tags import avatar, link

register = template.Library()


@register.simple_tag(takes_context=True)
def legend(context, legend=None, size=None, show_avatar=True, show_link=True, url=None):
    legend = legend or context.get('legend', context.get('user'))

    name = legend if legend.is_authenticated() else 'Anonymous'
    url = url or legend.get_absolute_url() if legend.is_authenticated() else reverse('join')

    legend_context = {
        'name': name,
        'url': url,
    }

    if show_avatar:
        if legend.is_authenticated() and legend.avatar:
            image = legend.get_avatar(size=size).url
        else:
            image = static('legends/images/anonymous.png')
        legend_context['avatar'] = avatar(image=image, name=name, url=url, classes=size)

    if show_link:
        legend_context['link'] = link(content=name, url=url)

    legend_template = 'legends/widgets/avatar.html'
    return render_to_string(legend_template, context=legend_context)


@register.simple_tag(takes_context=True)
def legend_link(context, legend=None, **kwargs):
    # if no legend is given take the legend from the context or else the user
    legend = legend or context.get('legend', context.get('user'))
    legend_context = {}
    if legend and legend.is_authenticated():
        legend_context.update({
            'content': legend,
            'url': legend.get_absolute_url(),
        })
    else:
        legend_context.update({
            'content': 'Anonymous',
            'url': reverse('join'),
        })
    legend_context.update(kwargs)
    template = 'widgets/link.html'
    return render_to_string(template, context=legend_context)


@register.simple_tag()
def npc(name):
    template = 'legends/widgets/legend.html'
    images = {
        'coralina': 'Coralina.png',
        'phoenix': 'phoenix.png',
        'eagle': 'eagle.png',
        'parrot': 'parrot.png',
        'monkey': 'monkey.png',
        'tiger': 'tiger.png',
        'dolphin': 'dolphin.png',
        'bear': 'bear.png',
    }
    names = {
        'coralina': 'Coralina',
        'phoenix': 'Light Phoenix Oracle',
        'eagle': 'Professor Eagle Scientist',
        'parrot': 'Moderating Parrot Poet',
        'monkey': 'Caring Monkey Mother',
        'tiger': 'Trillionaire Tiger Entrepreneur',
        'dolphin': 'Playful Dolphin Dancer',
        'bear': 'Healthy Bear Athlete',
    }
    image_name = images.get(name) or images.get(name.lower())
    full_name = names.get(name, name)
    context = {
        'name': full_name,
        'source': static('legends/images/npc/{image_name}'.format(image_name=image_name)),
        'classname': name,
    }
    return render_to_string(template, context)

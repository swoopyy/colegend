from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, RedirectView

from colegend.core.views import OwnedCreateView, OwnedUpdateView
from .models import Tag
from .forms import TagForm


class TagIndexView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'tags:list'


class TagListView(LoginRequiredMixin, ListView):
    template_name = 'tags/list.html'
    model = Tag
    context_object_name = 'tags'


class TagCreateView(LoginRequiredMixin, OwnedCreateView):
    template_name = 'tags/create.html'
    model = Tag
    form_class = TagForm


class TagDetailView(LoginRequiredMixin, DetailView):
    template_name = 'tags/detail.html'
    model = Tag


class TagUpdateView(LoginRequiredMixin, OwnedUpdateView):
    template_name = 'tags/update.html'
    model = Tag
    form_class = TagForm


class TagDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'tags/delete.html'
    model = Tag

    def get_success_url(self):
        object = self.get_object()
        return object.get_index_url()

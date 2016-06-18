from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, RedirectView

from colegend.core.views import OwnedCreateView, OwnedUpdateView, OwnedItemsMixin
from .models import Vision
from .forms import VisionForm


class VisionMixin(OwnedItemsMixin):
    """
    Default attributes and methods for vision related views.
    """
    model = Vision
    form_class = VisionForm

    def get_object(self, queryset=None):
        scope = self.kwargs.get('scope')
        user = self.request.user
        return user.visions.scope(user, scope)


class VisionIndexView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'visions:list'

    def get_redirect_url(self, *args, **kwargs):
        scope = Vision.SCOPE_MAP.get(Vision.DAY)
        return reverse('visions:detail', kwargs={'scope': scope})


class VisionListView(LoginRequiredMixin, VisionMixin, ListView):
    template_name = 'visions/list.html'
    context_object_name = 'visions'


class VisionCreateView(LoginRequiredMixin, VisionMixin, OwnedCreateView):
    template_name = 'visions/create.html'


class VisionDetailView(LoginRequiredMixin, VisionMixin, DetailView):
    template_name = 'visions/detail.html'


class VisionUpdateView(LoginRequiredMixin, VisionMixin, OwnedUpdateView):
    template_name = 'visions/update.html'


class VisionDeleteView(LoginRequiredMixin, VisionMixin, DeleteView):
    template_name = 'visions/delete.html'

    def get_success_url(self):
        vision = self.get_object()
        return vision.index_url
from django.conf.urls import url, include
from django.views.generic import RedirectView

from .views import GuideIntroductionView, GuideManageView, GuideDetailView, GuideListView, \
    GuideesView, GuideActionView, GuideView

__author__ = 'eraldo'

urlpatterns = [
    url(r'^$',
        RedirectView.as_view(url='list/', permanent=False),
        name='index'),
    url(r'^list/$',
        GuideListView.as_view(),
        name='list'),
    url(r'^introduction/$',
        GuideIntroductionView.as_view(),
        name='introduction'),
    url(r'^guide/$',
        GuideView.as_view(),
        name='guide'),
    url(r'^guidees/$',
        GuideesView.as_view(),
        name='guidees'),
    url(r'^(?P<owner>[\w.@+-]+)/$',
        GuideDetailView.as_view(),
        name='detail'),
    url(r'^(?P<owner>[\w.@+-]+)/manage/$',
        GuideManageView.as_view(),
        name='manage'),
    url(r'^(?P<owner>[\w.@+-]+)/guide/$',
        GuideActionView.as_view(),
        name='guide-action'),
]
urlpatterns = [
    url(r'^', include(urlpatterns, namespace='guides')),
]

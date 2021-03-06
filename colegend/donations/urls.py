from django.conf.urls import url

from .views import DonationIndexView, DonationListView, DonationCreateView, DonationDetailView, DonationUpdateView, \
    DonationDeleteView, TopSupportersListView

app_name = 'donations'
urlpatterns = [
    url(r'^$',
        DonationIndexView.as_view(),
        name='index'),
    url(r'^list/$',
        DonationListView.as_view(),
        name='list'),
    url(r'^create/$',
        DonationCreateView.as_view(),
        name='create'),
    url(r'^(?P<pk>[0-9]+)/$',
        DonationDetailView.as_view(),
        name='detail'),
    url(r'^(?P<pk>[0-9]+)/update/$',
        DonationUpdateView.as_view(),
        name='update'),
    url(r'^(?P<pk>[0-9]+)/delete/$',
        DonationDeleteView.as_view(),
        name='delete'),
    url(r'^top-supporters/$',
        TopSupportersListView.as_view(),
        name='top-supporters'),
]

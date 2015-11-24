from django.conf             import settings
from django.conf.urls.static import static
from django.conf.urls        import url
from .                       import views

urlpatterns = [
    url(r'^$',                                                   views.event_list),
    url(r'^list/(?P<period>[a-z]+)/$',                           views.event_list,            name='list'),
    url(r'^insert/$',                                            views.insert,                name='insert'),
    url(r'^booking/(?P<pk>[0-9]+)/(?P<attendance>[a-z]+)/$',     views.booking,               name='booking'),
    url(r'^update/(?P<pk>[0-9]+)/(?P<period>[a-z]+)/$',          views.update,                name='update'),
    url(r'^remove/(?P<pk>[0-9]+)/(?P<period>[a-z]+)/$',          views.remove,                name='remove'),
]

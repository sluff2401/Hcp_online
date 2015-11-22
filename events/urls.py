from django.conf             import settings
from django.conf.urls.static import static
from django.conf.urls        import url
from .                       import views

urlpatterns = [
    url(r'^$',                                                views.list,                  name='list'),
    #url(r'^past$',                                           views.list_past,             name='list_past'),
    url(r'^event/insert/$',                                   views.insert,                name='insert'),
    url(r'^event/(?P<pk>[0-9]+)/(?P<attendance>[a-z]+)/$',    views.booking,               name='booking'),
    url(r'^event/(?P<pk>[0-9]+)/update/$',                    views.update,                name='update'),
    url(r'^event/(?P<pk>[0-9]+)/remove/$',                    views.remove,                name='remove'),
]

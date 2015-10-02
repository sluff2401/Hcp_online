from django.conf             import settings
from django.conf.urls.static import static
from django.conf.urls        import url
from .                       import views

urlpatterns = [
    url(r'^$',                                  views.event_list,       name='event_list'),
    url(r'^event/(?P<pk>[0-9]+)/(?P<attendance>[a-z]+)/bookinto/$',    views.event_booking,  name='event_booking'),
    url(r'^event/(?P<pk>[0-9]+)/(?P<attendance>[a-z]+)/leave/$',       views.event_booking,      name='event_booking'),
] 

from django.conf             import settings
from django.conf.urls.static import static
from django.conf.urls        import url
from .                       import views

urlpatterns = [
    url(r'^$',                                                   views.event_list),
    url(r'^list/(?P<periodsought>[a-z]+)/$',                           views.event_list,            name='list'),
    url(r'^update/(?P<function>[a-z]+)/$',                         views.event_process,                name='insert'),
    url(r'^update/(?P<pk>[0-9]+)/(?P<function>[a-z]+)/$',          views.event_process,                name='update'),
    url(r'^insertuser/$',                                            views.insertuser,                name='insertuser'),
]

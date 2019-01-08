from django.conf.urls import url

from . import views as assets_views

app_name = 'assets'
urlpatterns = [
    url(r'^report/', assets_views.report, name = 'report'),
    url(r'^dashboard/', assets_views.dashboard, name = 'dashboard'),
    url(r'^index/', assets_views.index, name = 'index'),
    url(r'^detail/(?P<asset_id>[0-9]+)/$', assets_views.detail, name = 'detail'),
    url(r'^$', assets_views.dashboard),
]

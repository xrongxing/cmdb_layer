from django.conf.urls import url

from . import views as assets_views

app_name = 'assets'
urlpatterns = [
    url(r'report/', assets_views.report, name = 'report'),
]

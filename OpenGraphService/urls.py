from django.conf.urls import url

from .views import parse_from_url


urlpatterns = [
    url('parse/', parse_from_url),
    url('new_url', ''),
    url('new_url2', ''),
    url('new_url3', '')
]
from django.urls import re_path

from mock_api.dispatcher import Dispatcher


urlpatterns = [
    re_path(r'.*', Dispatcher().dispatch),
]

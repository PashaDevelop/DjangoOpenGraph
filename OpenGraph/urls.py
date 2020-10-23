from django.contrib import admin
from django.urls import path, include

from OpenGraphService.views import index

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('service/', include('OpenGraphService.urls'))
]

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('poll/', include('poll.urls', namespace='poll')),
    path('users/', include('users.urls', namespace='users')),
]

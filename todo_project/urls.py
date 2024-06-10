from django.contrib import admin
from django.urls import path, include
from . import codes_handler_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api', include('todos.urls')),
    path('api/auth/', include('rest_framework.urls')),  # For login and logout
]

handler404 = codes_handler_views.custom_404_view
handler500 = codes_handler_views.custom_500_view
handler403 = codes_handler_views.custom_403_view
handler400 = codes_handler_views.custom_400_view

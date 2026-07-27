from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from iot import views as iot_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', iot_views.logout_view, name='logout'),
    path('', iot_views.root_redirect, name='root_redirect'),
    path('', include('iot.urls')),
]




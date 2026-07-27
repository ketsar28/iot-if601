from django.urls import path
from . import views

urlpatterns = [
    path('api/sensor/', views.receive_sensor_data, name='receive_sensor_data'),
    path('api/sensor/<str:device_id>/', views.get_device_data_api, name='get_device_data_api'),
    path('device/<str:device_id>/', views.device_data_view, name='device_data_view'),
    path('device/<str:device_id>/gauge/', views.sensor_gauge_view, name='sensor_gauge_view'),

]

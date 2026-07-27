from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.utils.timezone import now, timedelta
from .models import SensorData
from .serializers import SensorDataSerializer
from .utils import is_valid_apikey

@api_view(['POST'])
def receive_sensor_data(request):
    data = request.data
    apikey = data.get("apikey")
    device_id = data.get("device_id")

    if not is_valid_apikey(apikey, device_id):
        return Response({"error": "Invalid API key"}, status=status.HTTP_403_FORBIDDEN)
    
    MAX_RECORDS = 100
    current_count = SensorData.objects.filter(device_id=request.data.get('device_id')).count()
    
    if current_count >= MAX_RECORDS:
        oldest = SensorData.objects.filter(device_id=request.data.get('device_id')).order_by('timestamp')[:1]
        oldest.delete()
        
    serializer = SensorDataSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Data saved"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_device_data_api(request, device_id):
    recent_data = SensorData.objects.filter(device_id=device_id).order_by('-timestamp')[:100]
    serializer = SensorDataSerializer(recent_data, many=True)
    return Response(serializer.data)

def device_data_view(request, device_id):
    recent_24h = now() - timedelta(hours=24)
    data = SensorData.objects.filter(device_id=device_id, timestamp__gte=recent_24h).order_by('-timestamp')[:100]
    return render(request, 'sensor_data.html', {'device_id': device_id, 'data': data})

def sensor_gauge_view(request, device_id):
    latest = SensorData.objects.filter(device_id=device_id).order_by('-timestamp').first()

    temp_ticks = [{'label': i, 'angle': (i / 50) * 180} for i in range(0, 51, 5)]
    hum_ticks = [{'label': i, 'angle': (i / 100) * 180} for i in range(0, 101, 10)]

    return render(request, 'sensor_gauge.html', {
        'device_id': device_id,
        'latest': latest,
        'temp_ticks': temp_ticks,
        'hum_ticks': hum_ticks,
    })

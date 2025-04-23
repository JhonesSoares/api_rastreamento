from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from datetime import timedelta
from django.utils import timezone

from .models import User, Vehicle, Location, Geofence, Alert, Report, Command
from .serializers import (
    UserSerializer, VehicleSerializer, LocationSerializer,
    GeofenceSerializer, AlertSerializer, ReportSerializer, CommandSerializer
)


class IsSuperOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.type == 'super' or obj.user == request.user

class UserViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated, IsSuperOrOwner) ## AUTENTICAÇÃO VAI TOKEN JWT
    queryset = User.objects.all()
    serializer_class = UserSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated, IsSuperOrOwner)
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


    @action(detail=True, methods=['get'])
    def recent_locations(self, request, pk=None):
        """
        Returns the vehicle's locations from the last 24 hours.
        """
        vehicle = self.get_object()

        if vehicle.status == 'offline':
            return Response({"detail": "Vehicle is offline and not sending location data."}, status=200)

        last_24_hours = timezone.now() - timedelta(days=1)
        locations = vehicle.locations.filter(timestamp__gte=last_24_hours)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
    

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class GeofenceViewSet(viewsets.ModelViewSet):
    queryset = Geofence.objects.all()
    serializer_class = GeofenceSerializer

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class CommandViewSet(viewsets.ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer
from datetime import timedelta
from math import asin, cos, radians, sin, sqrt

from django.shortcuts import render
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Location, User, Vehicle
from .serializers import LocationSerializer, UserSerializer, VehicleSerializer


# Create your views here.
def index(request):
    return render(request, "core/index.html")


class IsSuperOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.type == "super" or obj.user == request.user


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, IsSuperOrOwner) ## AUTENTICAÇÃO VAI TOKEN JWT
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, IsSuperOrOwner)
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    @action(detail=True, methods=["get"])
    def recent_locations(self, request, pk=None):
        """
        Retorna as localizações dos veículos das últimas 24 horas.
        """
        vehicle = self.get_object()

        if vehicle.status == "offline":
            return Response(
                {"detail": "Vehicle is offline and not sending location data."},
                status=200,
            )

        last_24_hours = timezone.now() - timedelta(days=1)
        locations = vehicle.locations.filter(timestamp__gte=last_24_hours)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def haversine(self, lat1, lon1, lat2, lon2):
        """
        A fórmula de Haversine calcula a distância entre dois pontos na Terra
        levando em conta a curvatura do planeta (geodésica).
        Raio da terra em metros
        """
        R = 6371000
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        return R * c

    def create(self, request, *args, **kwargs):
        """
        Método sobrescrito para Evitar que o banco de dados fique
        sobrecarregado com dados inúteis ou redundantes.
        Método que limita o evio de dados pa o banco Locations. (localização_recente < 10 metros)
        """
        data = request.data
        vehicle_id = data.get("vehicle")

        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
        except Vehicle.DoesNotExist:
            return Response({"detail": "Veículo não encontrado."}, status=404)

        last_location = vehicle.locations.order_by(
            "-timestamp"
        ).first()  # última localização

        if last_location:
            lat1 = float(data.get("latitude"))
            lon1 = float(data.get("longitude"))

            lat2 = last_location.latitude
            lon2 = last_location.longitude

            distance = self.haversine(lat1, lon1, lat2, lon2)
            time_diff = timezone.now() - last_location.timestamp
            print("Distância:", distance)
            print("Tempo decorrido:", time_diff)

            if distance < 10:
                data = {
                    "vehicle": request.data.get("vehicle"),
                    "latitude": float(request.data.get("latitude")),
                    "longitude": float(request.data.get("longitude")),
                    "speed": float(request.data.get("speed", 0.0)),
                }
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                print('"detail": "Registro ignorado: distância < 10m e tempo < 30s."')
                return Response(serializer.data, status=200)
                # return Response({"detail": "Registro ignorado: distância < 10m e tempo < 30s."}, status=200)

        return super().create(request, *args, **kwargs)

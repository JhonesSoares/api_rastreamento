from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, VehicleViewSet, LocationViewSet,
    GeofenceViewSet, AlertViewSet, ReportViewSet, CommandViewSet
)
from .views import index

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'geofences', GeofenceViewSet)
router.register(r'alerts', AlertViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'commands', CommandViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('index/', index, name='index'),
]
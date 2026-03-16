from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LocationViewSet, UserViewSet, VehicleViewSet, index

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"vehicles", VehicleViewSet)
router.register(r"locations", LocationViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("index/", index, name="index"),
]

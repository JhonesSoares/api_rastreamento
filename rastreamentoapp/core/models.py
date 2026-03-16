import uuid

from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    type = models.CharField(
        max_length=10, choices=[("super", "Super"), ("common", "Common")]
    )
    connected_devices = models.IntegerField(default=0)
    manager = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="managed_users",
    )

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicles")
    type_vehicle = models.CharField(
        blank=True,
        max_length=20,
        choices=[
            ("Ciclomotor", "Ciclomotor"),
            ("Motoneta", "Motoneta"),
            ("Motocicleta", "Motocicleta"),
            ("Triciclo", "Triciclo"),
            ("Quadriciclo", "Quadriciclo"),
            ("Automóvel", "Automóvel"),
            ("Microônibus", "Microônibus"),
            ("Ônibus", "Ônibus"),
        ],
    )
    plate = models.CharField(max_length=10, unique=True)
    model = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10, choices=[("online", "Online"), ("offline", "Offline")]
    )
    current_speed = models.FloatField(default=0.0)
    current_location = models.OneToOneField(
        "Location", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    def __str__(self):
        return f"{self.user} ({self.type_vehicle}: {self.model} - {self.plate})"


class Location(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="locations"
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle.user} ({self.vehicle.type_vehicle}: {self.vehicle.model}-{self.vehicle.plate}, Localização: {self.latitude}, {self.longitude})"

from django.db import models
import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=[('super', 'Super'), ('common', 'Common')])
    connected_devices = models.IntegerField(default=0)
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='managed_users')

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    type_vehicle = models.CharField(
        blank=True,
        max_length=20,
        choices=[
            ('Ciclomotor', 'Ciclomotor'),
            ('Motoneta', 'Motoneta'),
            ('Motocicleta', 'Motocicleta'),
            ('Triciclo', 'Triciclo'),
            ('Quadriciclo', 'Quadriciclo'),
            ('Automóvel','Automóvel'),
            ('Microônibus', 'Microônibus'),
            ('Ônibus', 'Ônibus'),
        ]
    )
    plate = models.CharField(max_length=10, unique=True)
    model = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=[('online', 'Online'), ('offline', 'Offline')])
    current_speed = models.FloatField(default=0.0)
    current_location = models.OneToOneField('Location', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    def __str__(self):
        return f"{self.user} ({self.type_vehicle}: {self.model} - {self.plate})"

class Location(models.Model):

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle.user} ({self.vehicle.type_vehicle}: {self.vehicle.model}-{self.vehicle.plate}, Localização: {self.latitude}, {self.longitude})"

class Geofence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='geofences')
    name = models.CharField(max_length=100)
    radius = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()

class Alert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='alerts')
    type = models.CharField(max_length=50)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    content = models.TextField()  # or use FileField for PDF/Excel

class Command(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    sent_at = models.DateTimeField(auto_now_add=True)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_commands')
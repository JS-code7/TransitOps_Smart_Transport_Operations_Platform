import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


class SyncStatus(models.TextChoices):
    ACTIVE = 'Active', 'Active'
    IN_SERVICE = 'In Service', 'In Service'
    MAINTENANCE = 'Maintenance', 'Maintenance'
    IDLE = 'Idle', 'Idle'
    RETIRED = 'Retired', 'Retired'
    ON_DUTY = 'On Duty', 'On Duty'
    OFF_DUTY = 'Off Duty', 'Off Duty'
    SICK = 'Sick', 'Sick'
    SUSPENDED = 'Suspended', 'Suspended'
    PENDING = 'Pending', 'Pending'
    LOADING = 'Loading', 'Loading'
    ON_ROUTE = 'On Route', 'On Route'
    DELAYED = 'Delayed', 'Delayed'
    COMPLETED = 'Completed', 'Completed'
    CANCELLED = 'Cancelled', 'Cancelled'
    IN_PROGRESS = 'In Progress', 'In Progress'
    RESOLVED = 'Resolved', 'Resolved'


class VehicleType(models.TextChoices):
    HEAVY_TRUCK = 'Heavy Truck', 'Heavy Truck'
    DELIVERY_VAN = 'Delivery Van', 'Delivery Van'
    ELECTRIC_CARRIER = 'Electric Carrier', 'Electric Carrier'


class ExpenseCategory(models.TextChoices):
    FUEL = 'Fuel', 'Fuel'
    MAINTENANCE = 'Maintenance', 'Maintenance'
    DRIVER_SALARY = 'Driver Salary', 'Driver Salary'
    INSURANCE = 'Insurance', 'Insurance'
    TOLLS_PERMITS = 'Tolls & Permits', 'Tolls & Permits'
    OTHER = 'Other', 'Other'


class PriorityLevel(models.TextChoices):
    LOW = 'Low', 'Low'
    MEDIUM = 'Medium', 'Medium'
    CRITICAL = 'Critical', 'Critical'


class ThemeChoice(models.TextChoices):
    LIGHT = 'Light', 'Light'
    SLATE = 'Slate', 'Slate'
    DARK = 'Dark', 'Dark'


class DensityChoice(models.TextChoices):
    HIGH = 'High', 'High'
    COMPACT = 'Compact', 'Compact'
    STANDARD = 'Standard', 'Standard'


class RoleChoice(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    DRIVER = 'Driver', 'Driver'


class IdPrefixedModel(models.Model):
    id = models.CharField(max_length=32, primary_key=True, editable=False)
    id_prefix = 'x'

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f'{self.id_prefix}-{uuid.uuid4().hex[:10]}'
        super().save(*args, **kwargs)


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Vehicle(IdPrefixedModel, TimestampedModel):
    id_prefix = 'v'
    name = models.CharField(max_length=120)
    plate = models.CharField(max_length=40, unique=True)
    type = models.CharField(max_length=40, choices=VehicleType.choices)
    status = models.CharField(max_length=24, choices=SyncStatus.choices, default=SyncStatus.ACTIVE)
    fuel = models.FloatField(default=100)
    health = models.FloatField(default=100)
    capacity = models.CharField(max_length=40)
    last_service = models.DateField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.name} ({self.plate})'


class Driver(IdPrefixedModel, TimestampedModel):
    id_prefix = 'd'
    name = models.CharField(max_length=120)
    license = models.CharField(max_length=40, unique=True)
    safety_score = models.IntegerField(default=95)
    status = models.CharField(max_length=24, choices=SyncStatus.choices, default=SyncStatus.ACTIVE)
    hours = models.IntegerField(default=0)
    phone = models.CharField(max_length=40)
    avatar_color = models.CharField(max_length=32, default='bg-indigo-600')
    email = models.EmailField(blank=True, null=True, unique=True)
    license_category = models.CharField(max_length=60, blank=True, default='')
    license_expiry = models.DateField(blank=True, null=True)
    experience = models.CharField(max_length=60, blank=True, default='')
    total_distance = models.IntegerField(default=0)
    fuel_efficiency = models.CharField(max_length=40, blank=True, default='')
    achievements = models.JSONField(default=list, blank=True)
    recent_activity = models.JSONField(default=list, blank=True)
    performance_timeline = models.JSONField(default=list, blank=True)
    upcoming_trips_count = models.IntegerField(default=0)
    today_distance = models.IntegerField(default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Trip(IdPrefixedModel, TimestampedModel):
    id_prefix = 'TR'
    vehicle_id = models.CharField(max_length=32)
    driver_id = models.CharField(max_length=32)
    destination = models.CharField(max_length=120)
    departure = models.CharField(max_length=120)
    status = models.CharField(max_length=24, choices=SyncStatus.choices, default=SyncStatus.PENDING)
    eta = models.CharField(max_length=60)
    progress = models.IntegerField(default=0)
    freight = models.CharField(max_length=160)
    cost = models.FloatField(default=0)
    date = models.DateField()

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f'TR-{uuid.uuid4().hex[:4].upper()}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id


class MaintenanceRecord(IdPrefixedModel, TimestampedModel):
    id_prefix = 'm'
    vehicle_id = models.CharField(max_length=32)
    type = models.CharField(max_length=120)
    priority = models.CharField(max_length=24, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    status = models.CharField(max_length=24, choices=SyncStatus.choices, default=SyncStatus.PENDING)
    cost = models.FloatField(default=0)
    date = models.DateField()
    technician = models.CharField(max_length=120)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.type


class FuelLog(IdPrefixedModel, TimestampedModel):
    id_prefix = 'f'
    vehicle_id = models.CharField(max_length=32)
    volume = models.FloatField(default=0)
    price_per_unit = models.FloatField(default=0)
    total_cost = models.FloatField(default=0)
    odometer = models.IntegerField(default=0)
    station = models.CharField(max_length=120)
    date = models.DateField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.station


class Expense(IdPrefixedModel, TimestampedModel):
    id_prefix = 'e'
    category = models.CharField(max_length=40, choices=ExpenseCategory.choices)
    amount = models.FloatField(default=0)
    date = models.DateField()
    description = models.CharField(max_length=255)
    reference = models.CharField(max_length=80)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.reference


class Notification(IdPrefixedModel, TimestampedModel):
    id_prefix = 'n'
    title = models.CharField(max_length=120)
    message = models.CharField(max_length=255)
    time = models.CharField(max_length=40)
    unread = models.BooleanField(default=True)
    type = models.CharField(max_length=24, default='info')

    class Meta:
        ordering = ['id']


class SystemSettings(models.Model):
    id = models.CharField(max_length=16, primary_key=True, default='default', editable=False)
    org_name = models.CharField(max_length=160)
    address = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=64)
    currency = models.CharField(max_length=40)
    timezone = models.CharField(max_length=80)
    notifications_enabled = models.BooleanField(default=True)
    density = models.CharField(max_length=20, choices=DensityChoice.choices, default=DensityChoice.HIGH)
    theme = models.CharField(max_length=20, choices=ThemeChoice.choices, default=ThemeChoice.LIGHT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=RoleChoice.choices, default=RoleChoice.ADMIN)
    driver_id = models.CharField(max_length=32, blank=True, default='')
    display_name = models.CharField(max_length=120, blank=True, default='')

    def to_session(self):
        return {
            'email': self.user.email or self.user.username,
            'name': self.display_name or self.user.get_full_name() or self.user.username,
            'role': self.role,
            'driverId': self.driver_id or None,
        }

    def __str__(self):
        return f'{self.user.username} ({self.role})'

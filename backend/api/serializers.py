from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (
    Driver,
    Expense,
    FuelLog,
    MaintenanceRecord,
    Notification,
    SystemSettings,
    Trip,
    UserProfile,
    Vehicle,
)


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = '__all__'


class FuelLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelLog
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class SystemSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSettings
        fields = '__all__'


class UserSessionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    role = serializers.ChoiceField(choices=['Admin', 'Driver'])
    driverId = serializers.CharField(allow_null=True, required=False)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=['Admin', 'Driver'])
    name = serializers.CharField()
    driverId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    password = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)


User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role', 'driver_id', 'display_name']

from django.contrib import admin

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


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'plate', 'type', 'status', 'fuel', 'health')
    search_fields = ('id', 'name', 'plate')


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'license', 'status', 'safety_score')
    search_fields = ('id', 'name', 'license', 'email')


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_id', 'driver_id', 'status', 'destination', 'date')
    search_fields = ('id', 'vehicle_id', 'driver_id', 'destination')


@admin.register(MaintenanceRecord)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_id', 'type', 'priority', 'status', 'date')


@admin.register(FuelLog)
class FuelLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_id', 'station', 'date', 'total_cost')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'amount', 'reference', 'date')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'unread', 'time')


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'org_name', 'theme', 'density')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'driver_id', 'display_name')

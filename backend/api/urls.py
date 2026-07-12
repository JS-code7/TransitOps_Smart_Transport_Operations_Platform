from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    DriverViewSet,
    ExpenseViewSet,
    FuelLogViewSet,
    LoginView,
    LogoutView,
    MaintenanceViewSet,
    NotificationViewSet,
    SessionView,
    SettingsViewSet,
    SnapshotView,
    TripViewSet,
    VehicleViewSet,
)

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicles')
router.register(r'drivers', DriverViewSet, basename='drivers')
router.register(r'trips', TripViewSet, basename='trips')
router.register(r'maintenance', MaintenanceViewSet, basename='maintenance')
router.register(r'fuel-logs', FuelLogViewSet, basename='fuel-logs')
router.register(r'expenses', ExpenseViewSet, basename='expenses')
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'settings', SettingsViewSet, basename='settings')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/session/', SessionView.as_view(), name='auth-session'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('snapshot/', SnapshotView.as_view(), name='snapshot'),
]

urlpatterns += router.urls

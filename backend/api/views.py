from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.dateparse import parse_date
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

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
from .serializers import (
    DriverSerializer,
    ExpenseSerializer,
    FuelLogSerializer,
    LoginSerializer,
    MaintenanceRecordSerializer,
    NotificationSerializer,
    SystemSettingsSerializer,
    TripSerializer,
    UserSessionSerializer,
    VehicleSerializer,
)


class CollectionSyncMixin:
    def _normalize_items(self, request):
        if isinstance(request.data, list):
            return request.data
        if isinstance(request.data, dict) and 'items' in request.data:
            return request.data['items']
        return []

    @action(detail=False, methods=['put'], url_path='sync')
    def sync(self, request):
        items = self._normalize_items(request)
        serializer = self.get_serializer(data=items, many=True)

        from rest_framework.validators import UniqueValidator
        child = getattr(serializer, 'child', serializer)
        for field in child.fields.values():
            field.validators = [v for v in field.validators if not isinstance(v, UniqueValidator)]

        serializer.is_valid(raise_exception=True)

        model = self.get_queryset().model
        with transaction.atomic():
            self.get_queryset().delete()
            for item in serializer.validated_data:
                model.objects.create(**item)

        return Response(self.get_serializer(self.get_queryset(), many=True).data)


class BaseCollectionViewSet(CollectionSyncMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.order_by('id')


class VehicleViewSet(BaseCollectionViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class DriverViewSet(BaseCollectionViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class TripViewSet(BaseCollectionViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class MaintenanceViewSet(BaseCollectionViewSet):
    queryset = MaintenanceRecord.objects.all()
    serializer_class = MaintenanceRecordSerializer


class FuelLogViewSet(BaseCollectionViewSet):
    queryset = FuelLog.objects.all()
    serializer_class = FuelLogSerializer


class ExpenseViewSet(BaseCollectionViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class NotificationViewSet(BaseCollectionViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class SettingsViewSet(CollectionSyncMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SystemSettings.objects.all()
    serializer_class = SystemSettingsSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.order_by('id')

    def perform_create(self, serializer):
        serializer.save(id='default')

    @action(detail=False, methods=['put'], url_path='sync')
    def sync(self, request):
        items = self._normalize_items(request)
        if not items:
            return Response([], status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=[items[0]], many=True)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            self.get_queryset().delete()
            settings_data = dict(serializer.validated_data[0])
            settings_data.pop('id', None)
            SystemSettings.objects.create(id='default', **settings_data)

        return Response(self.get_serializer(self.get_queryset(), many=True).data)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email = data['email'].strip().lower()
        role = data['role']
        display_name = data['name']
        driver_id = (data.get('driverId') or '').strip()

        User = get_user_model()
        username = email or display_name.lower().replace(' ', '.')
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'first_name': display_name},
        )
        if email and user.email != email:
            user.email = email
        if display_name and user.first_name != display_name:
            user.first_name = display_name
        if created and data.get('password'):
            user.set_password(data['password'])
        elif created:
            user.set_unusable_password()
        user.is_staff = role == 'Admin'
        user.save()

        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = role
        profile.display_name = display_name
        profile.driver_id = driver_id if role == 'Driver' else ''
        profile.save()

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': profile.to_session()})


class SessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'role': 'Admin' if request.user.is_staff else 'Driver',
                'display_name': request.user.get_full_name() or request.user.first_name or request.user.username,
                'driver_id': 'd-alex' if not request.user.is_staff else '',
            },
        )
        return Response({'user': profile.to_session()})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SnapshotView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            {
                'vehicles': VehicleSerializer(Vehicle.objects.order_by('id'), many=True).data,
                'drivers': DriverSerializer(Driver.objects.order_by('id'), many=True).data,
                'trips': TripSerializer(Trip.objects.order_by('id'), many=True).data,
                'maintenance': MaintenanceRecordSerializer(MaintenanceRecord.objects.order_by('id'), many=True).data,
                'fuelLogs': FuelLogSerializer(FuelLog.objects.order_by('id'), many=True).data,
                'expenses': ExpenseSerializer(Expense.objects.order_by('id'), many=True).data,
                'notifications': NotificationSerializer(Notification.objects.order_by('id'), many=True).data,
                'settings': SystemSettingsSerializer(SystemSettings.objects.order_by('id').first()).data if SystemSettings.objects.exists() else None,
            }
        )

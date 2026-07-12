from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from api.models import (
    Driver,
    Expense,
    FuelLog,
    MaintenanceRecord,
    Notification,
    RoleChoice,
    SystemSettings,
    Trip,
    UserProfile,
    Vehicle,
)


class Command(BaseCommand):
    help = 'Seed the TransitOps database with frontend-matching demo data.'

    def handle(self, *args, **options):
        User = get_user_model()
        with transaction.atomic():
            Notification.objects.all().delete()
            Expense.objects.all().delete()
            FuelLog.objects.all().delete()
            MaintenanceRecord.objects.all().delete()
            Trip.objects.all().delete()
            Driver.objects.all().delete()
            Vehicle.objects.all().delete()
            SystemSettings.objects.all().delete()
            UserProfile.objects.all().delete()
            User.objects.filter(username__in=['admin@transitops.com', 'alex@transitops.com']).delete()

            vehicles = [
                Vehicle(id='v-1', name='Volvo FH16', plate='AX-902-KL', type='Heavy Truck', status='Active', fuel=85, health=94, capacity='25 Tons', last_service=date(2026, 6, 15)),
                Vehicle(id='v-2', name='Scania R450', plate='TY-341-PP', type='Heavy Truck', status='In Service', fuel=62, health=89, capacity='24 Tons', last_service=date(2026, 5, 20)),
                Vehicle(id='v-3', name='Ford Transit', plate='ER-881-QQ', type='Delivery Van', status='Maintenance', fuel=35, health=68, capacity='3.5 Tons', last_service=date(2026, 7, 10)),
                Vehicle(id='v-4', name='Rivian EDV', plate='EV-772-DX', type='Electric Carrier', status='Active', fuel=95, health=99, capacity='2.0 Tons', last_service=date(2026, 7, 8)),
            ]
            for vehicle in vehicles:
                vehicle.save()

            drivers = [
                Driver(id='d-1', name='Robert Vance', license='CDL-A-8821', safety_score=98, status='On Duty', hours=142, phone='+1 (555) 321-4567', avatar_color='bg-indigo-600'),
                Driver(id='d-2', name='Arun Singh', license='CDL-A-4190', safety_score=94, status='On Duty', hours=118, phone='+1 (555) 890-1234', avatar_color='bg-purple-600'),
                Driver(id='d-3', name='Sarah Parker', license='CDL-B-5532', safety_score=96, status='Active', hours=160, phone='+1 (555) 765-4321', avatar_color='bg-emerald-600'),
                Driver(id='d-4', name='Leo Gaultier', license='CDL-A-9912', safety_score=78, status='Off Duty', hours=110, phone='+1 (555) 234-5678', avatar_color='bg-amber-600'),
                Driver(
                    id='d-alex',
                    name='Alex Rivera',
                    license='CDL-A-9942',
                    safety_score=97,
                    status='On Duty',
                    hours=145,
                    phone='+1 (555) 432-8890',
                    avatar_color='bg-[#5B3DF5]',
                    email='alex@transitops.com',
                    license_category='CDL Class A',
                    license_expiry=date(2028, 11, 15),
                    experience='8 Years',
                    total_distance=12450,
                    fuel_efficiency='6.8 MPG',
                    achievements=['Safe Driver of the Month', 'Eco-Hauler Certified', 'Zero Incidents 2025'],
                    recent_activity=['Logged fuel volume at Pilot Center Denver', 'Completed cargo transit route TR-8944', 'Pre-trip checks approved'],
                    performance_timeline=[
                        {'date': 'Mon', 'score': 95},
                        {'date': 'Tue', 'score': 96},
                        {'date': 'Wed', 'score': 98},
                        {'date': 'Thu', 'score': 97},
                        {'date': 'Fri', 'score': 97},
                    ],
                    upcoming_trips_count=3,
                    today_distance=245,
                ),
            ]
            for driver in drivers:
                driver.save()

            trips = [
                Trip(id='TR-8942', vehicle_id='v-1', driver_id='d-alex', destination='Chicago, IL', departure='St. Louis, MO', status='On Route', eta='14:20 PM', progress=75, freight='Industrial Equipment', cost=1450, date=date(2026, 7, 11)),
                Trip(id='TR-8943', vehicle_id='v-2', driver_id='d-2', destination='New York, NY', departure='Philadelphia, PA', status='Loading', eta='16:45 PM', progress=15, freight='Consumer Goods', cost=850, date=date(2026, 7, 11)),
                Trip(id='TR-8944', vehicle_id='v-4', driver_id='d-3', destination='Seattle, WA', departure='Portland, OR', status='Completed', eta='Done', progress=100, freight='Medical Supplies', cost=500, date=date(2026, 7, 10)),
                Trip(id='TR-8945', vehicle_id='v-1', driver_id='d-alex', destination='Denver, CO', departure='Chicago, IL', status='Pending', eta='Tomorrow 08:00 AM', progress=0, freight='Automotive Parts', cost=2100, date=date(2026, 7, 13)),
            ]
            for trip in trips:
                trip.save()

            maintenance = [
                MaintenanceRecord(id='m-1', vehicle_id='v-3', type='Brake Overhaul', priority='Critical', status='In Progress', cost=850, date=date(2026, 7, 10), technician='Elite Truck Service'),
                MaintenanceRecord(id='m-2', vehicle_id='v-2', type='Engine Tuning', priority='Medium', status='Pending', cost=420, date=date(2026, 7, 15), technician='McGrath Mechanics'),
            ]
            for record in maintenance:
                record.save()

            fuel_logs = [
                FuelLog(id='f-1', vehicle_id='v-1', volume=120, price_per_unit=3.85, total_cost=462, odometer=145800, station='Shell St. Louis', date=date(2026, 7, 9)),
                FuelLog(id='f-2', vehicle_id='v-2', volume=145, price_per_unit=3.92, total_cost=568.4, odometer=92310, station='Pilot Center Denver', date=date(2026, 7, 8)),
            ]
            for fuel_log in fuel_logs:
                fuel_log.save()

            expenses = [
                Expense(id='e-1', category='Fuel', amount=1030.4, date=date(2026, 7, 9), description='Fleet fuel bulk refills', reference='INV-9942'),
                Expense(id='e-2', category='Maintenance', amount=850.0, date=date(2026, 7, 10), description='Volvo Brake System Overhaul', reference='INV-8831'),
                Expense(id='e-3', category='Driver Salary', amount=3200.0, date=date(2026, 7, 5), description='Bi-weekly Driver payroll', reference='PAY-2291'),
            ]
            for expense in expenses:
                expense.save()

            notifications = [
                Notification(id='1', title='Route Delayed', message='Trip TR-8942 is currently delayed near Chicago.', time='5m ago', unread=True, type='warning'),
                Notification(id='2', title='Low Fuel Warning', message='Vehicle AX-902-KL fuel telemetry drops under 15%.', time='12m ago', unread=True, type='danger'),
                Notification(id='3', title='Odometer Update', message='Driver Sarah Parker synced vehicle Rivian EDV.', time='1h ago', unread=False, type='info'),
            ]
            for notification in notifications:
                notification.save()

            SystemSettings.objects.create(
                id='default',
                org_name='TransitOps Logistics Ltd',
                address='450 Terminal Pkwy, Sector 4, Chicago IL',
                tax_id='TX-882-901-A',
                currency='USD ($)',
                timezone='UTC-6 (Central Standard Time)',
                notifications_enabled=True,
                density='High',
                theme='Light',
            )

            admin_user = User.objects.create_user(username='admin@transitops.com', email='admin@transitops.com')
            admin_user.set_unusable_password()
            admin_user.is_staff = True
            admin_user.save(update_fields=['password', 'is_staff'])
            UserProfile.objects.create(user=admin_user, role=RoleChoice.ADMIN, display_name='James Donovan')

            driver_user = User.objects.create_user(username='alex@transitops.com', email='alex@transitops.com')
            driver_user.set_unusable_password()
            driver_user.save(update_fields=['password'])
            UserProfile.objects.create(user=driver_user, role=RoleChoice.DRIVER, driver_id='d-alex', display_name='Alex Rivera')

        self.stdout.write(self.style.SUCCESS('TransitOps demo data seeded successfully.'))
from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from api.models import (
    Driver,
    Expense,
    FuelLog,
    MaintenanceRecord,
    Notification,
    RoleChoice,
    SystemSettings,
    Trip,
    UserProfile,
    Vehicle,
)


class Command(BaseCommand):
    help = 'Seed the TransitOps database with frontend-matching demo data.'

    def handle(self, *args, **options):
        User = get_user_model()
        with transaction.atomic():
            Notification.objects.all().delete()
            Expense.objects.all().delete()
            FuelLog.objects.all().delete()
            MaintenanceRecord.objects.all().delete()
            Trip.objects.all().delete()
            Driver.objects.all().delete()
            Vehicle.objects.all().delete()
            SystemSettings.objects.all().delete()
            UserProfile.objects.all().delete()
            User.objects.filter(username__in=['admin@transitops.com', 'alex@transitops.com']).delete()

            vehicles = [
                Vehicle(id='v-1', name='Volvo FH16', plate='AX-902-KL', type='Heavy Truck', status='Active', fuel=85, health=94, capacity='25 Tons', last_service=date(2026, 6, 15)),
                Vehicle(id='v-2', name='Scania R450', plate='TY-341-PP', type='Heavy Truck', status='In Service', fuel=62, health=89, capacity='24 Tons', last_service=date(2026, 5, 20)),
                Vehicle(id='v-3', name='Ford Transit', plate='ER-881-QQ', type='Delivery Van', status='Maintenance', fuel=35, health=68, capacity='3.5 Tons', last_service=date(2026, 7, 10)),
                Vehicle(id='v-4', name='Rivian EDV', plate='EV-772-DX', type='Electric Carrier', status='Active', fuel=95, health=99, capacity='2.0 Tons', last_service=date(2026, 7, 8)),
            ]
            for vehicle in vehicles:
                vehicle.save()

            drivers = [
                Driver(id='d-1', name='Robert Vance', license='CDL-A-8821', safety_score=98, status='On Duty', hours=142, phone='+1 (555) 321-4567', avatar_color='bg-indigo-600'),
                Driver(id='d-2', name='Arun Singh', license='CDL-A-4190', safety_score=94, status='On Duty', hours=118, phone='+1 (555) 890-1234', avatar_color='bg-purple-600'),
                Driver(id='d-3', name='Sarah Parker', license='CDL-B-5532', safety_score=96, status='Active', hours=160, phone='+1 (555) 765-4321', avatar_color='bg-emerald-600'),
                Driver(id='d-4', name='Leo Gaultier', license='CDL-A-9912', safety_score=78, status='Off Duty', hours=110, phone='+1 (555) 234-5678', avatar_color='bg-amber-600'),
                Driver(
                    id='d-alex',
                    name='Alex Rivera',
                    license='CDL-A-9942',
                    safety_score=97,
                    status='On Duty',
                    hours=145,
                    phone='+1 (555) 432-8890',
                    avatar_color='bg-[#5B3DF5]',
                    email='alex@transitops.com',
                    license_category='CDL Class A',
                    license_expiry=date(2028, 11, 15),
                    experience='8 Years',
                    total_distance=12450,
                    fuel_efficiency='6.8 MPG',
                    achievements=['Safe Driver of the Month', 'Eco-Hauler Certified', 'Zero Incidents 2025'],
                    recent_activity=['Logged fuel volume at Pilot Center Denver', 'Completed cargo transit route TR-8944', 'Pre-trip checks approved'],
                    performance_timeline=[
                        {'date': 'Mon', 'score': 95},
                        {'date': 'Tue', 'score': 96},
                        {'date': 'Wed', 'score': 98},
                        {'date': 'Thu', 'score': 97},
                        {'date': 'Fri', 'score': 97},
                    ],
                    upcoming_trips_count=3,
                    today_distance=245,
                ),
            ]
            for driver in drivers:
                driver.save()

            trips = [
                Trip(id='TR-8942', vehicle_id='v-1', driver_id='d-alex', destination='Chicago, IL', departure='St. Louis, MO', status='On Route', eta='14:20 PM', progress=75, freight='Industrial Equipment', cost=1450, date=date(2026, 7, 11)),
                Trip(id='TR-8943', vehicle_id='v-2', driver_id='d-2', destination='New York, NY', departure='Philadelphia, PA', status='Loading', eta='16:45 PM', progress=15, freight='Consumer Goods', cost=850, date=date(2026, 7, 11)),
                Trip(id='TR-8944', vehicle_id='v-4', driver_id='d-3', destination='Seattle, WA', departure='Portland, OR', status='Completed', eta='Done', progress=100, freight='Medical Supplies', cost=500, date=date(2026, 7, 10)),
                Trip(id='TR-8945', vehicle_id='v-1', driver_id='d-alex', destination='Denver, CO', departure='Chicago, IL', status='Pending', eta='Tomorrow 08:00 AM', progress=0, freight='Automotive Parts', cost=2100, date=date(2026, 7, 13)),
            ]
            for trip in trips:
                trip.save()

            maintenance = [
                MaintenanceRecord(id='m-1', vehicle_id='v-3', type='Brake Overhaul', priority='Critical', status='In Progress', cost=850, date=date(2026, 7, 10), technician='Elite Truck Service'),
                MaintenanceRecord(id='m-2', vehicle_id='v-2', type='Engine Tuning', priority='Medium', status='Pending', cost=420, date=date(2026, 7, 15), technician='McGrath Mechanics'),
            ]
            for record in maintenance:
                record.save()

            fuel_logs = [
                FuelLog(id='f-1', vehicle_id='v-1', volume=120, price_per_unit=3.85, total_cost=462, odometer=145800, station='Shell St. Louis', date=date(2026, 7, 9)),
                FuelLog(id='f-2', vehicle_id='v-2', volume=145, price_per_unit=3.92, total_cost=568.4, odometer=92310, station='Pilot Center Denver', date=date(2026, 7, 8)),
            ]
            for fuel_log in fuel_logs:
                fuel_log.save()

            expenses = [
                Expense(id='e-1', category='Fuel', amount=1030.4, date=date(2026, 7, 9), description='Fleet fuel bulk refills', reference='INV-9942'),
                Expense(id='e-2', category='Maintenance', amount=850.0, date=date(2026, 7, 10), description='Volvo Brake System Overhaul', reference='INV-8831'),
                Expense(id='e-3', category='Driver Salary', amount=3200.0, date=date(2026, 7, 5), description='Bi-weekly Driver payroll', reference='PAY-2291'),
            ]
            for expense in expenses:
                expense.save()

            notifications = [
                Notification(id='1', title='Route Delayed', message='Trip TR-8942 is currently delayed near Chicago.', time='5m ago', unread=True, type='warning'),
                Notification(id='2', title='Low Fuel Warning', message='Vehicle AX-902-KL fuel telemetry drops under 15%.', time='12m ago', unread=True, type='danger'),
                Notification(id='3', title='Odometer Update', message='Driver Sarah Parker synced vehicle Rivian EDV.', time='1h ago', unread=False, type='info'),
            ]
            for notification in notifications:
                notification.save()

            SystemSettings.objects.create(
                id='default',
                org_name='TransitOps Logistics Ltd',
                address='450 Terminal Pkwy, Sector 4, Chicago IL',
                tax_id='TX-882-901-A',
                currency='USD ($)',
                timezone='UTC-6 (Central Standard Time)',
                notifications_enabled=True,
                density='High',
                theme='Light',
            )

            admin_user = User.objects.create_user(username='admin@transitops.com', email='admin@transitops.com')
            admin_user.set_unusable_password()
            admin_user.is_staff = True
            admin_user.save(update_fields=['password', 'is_staff'])
            UserProfile.objects.create(user=admin_user, role=RoleChoice.ADMIN, display_name='James Donovan')

            driver_user = User.objects.create_user(username='alex@transitops.com', email='alex@transitops.com')
            driver_user.set_unusable_password()
            driver_user.save(update_fields=['password'])
            UserProfile.objects.create(user=driver_user, role=RoleChoice.DRIVER, driver_id='d-alex', display_name='Alex Rivera')

        self.stdout.write(self.style.SUCCESS('TransitOps demo data seeded successfully.'))

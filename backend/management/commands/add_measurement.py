from django.core.management.base import BaseCommand
from backend.models import Device, Measurement
from datetime import datetime


class Command(BaseCommand):
    help = 'Add a measurement for a device'

    def add_arguments(self, parser):
        parser.add_argument('device_id', type=int, help='ID of the device')
        parser.add_argument('value', type=float, help='Measurement value (watts)')

    def handle(self, *args, **options):
        device_id = options['device_id']
        value = options['value']

        try:
            device = Device.objects.get(id=device_id)
        except Device.DoesNotExist:
            self.stderr.write(f"Device with ID {device_id} does not exist")
            return

        # Create new measurement (notification will be triggered automatically by signal)
        measurement = Measurement.objects.create(
            device=device,
            value=value,
            timestamp=datetime.now()
        )

        self.stdout.write(
            self.style.SUCCESS(f"Created measurement: {measurement}")
        )

        # Check if notification was created
        from backend.models import Notification
        recent_notifications = Notification.objects.filter(
            device=device,
            measurement=measurement
        ).count()

        if recent_notifications > 0:
            self.stdout.write(
                self.style.WARNING(f"NOTIFICATION TRIGGERED! ({recent_notifications} created)")
            )
        else:
            self.stdout.write("No notification triggered")
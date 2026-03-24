from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Measurement, Notification

# Threshold for notification (same as MQTT client)
JUMP_THRESHOLD_WATTS = 1000

@receiver(post_save, sender=Measurement)
def check_for_notification(sender, instance, created, **kwargs):
    """
    Check if a new measurement triggers a notification based on wattage jump.
    Only runs on creation (not updates) and only if there's a previous measurement.
    """
    if not created:
        return  # Only check on new measurements

    # Get the previous measurement for this device
    previous = Measurement.objects.filter(
        device=instance.device,
        timestamp__lt=instance.timestamp
    ).order_by("-timestamp").first()

    if previous is None:
        return  # No previous measurement to compare

    # Calculate the difference
    delta = abs(instance.value - previous.value)

    # Check if it exceeds the threshold
    if delta >= JUMP_THRESHOLD_WATTS:
        message = (
            f"Significant jump detected for device {instance.device.id}: "
            f"{previous.value}W -> {instance.value}W (Δ={delta}W)"
        )

        # Create the notification
        Notification.objects.create(
            device=instance.device,
            measurement=instance,
            message=message,
        )
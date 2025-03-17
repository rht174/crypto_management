import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Organization

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Organization)
def log_organization_created(sender, instance, created, **kwargs):
    if created:
        logger.info(
            f"Organization created - ID: {instance.id}, "
            f"Name: {instance.name}, "
            f"Owner: {instance.owner.username}"
        )


@receiver(post_delete, sender=Organization)
def log_organization_deleted(sender, instance, **kwargs):
    logger.info(
        f"Organization deleted - ID: {instance.id}, "
        f"Name: {instance.name}, "
        f"Owner: {instance.owner.username}"
    )

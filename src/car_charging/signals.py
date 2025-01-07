import logging
from django.db.models.signals import post_save, post_delete

from car_charging.models import ChargingSession, CostDetails, EnergyDetails, GridPrice, SpotPrice, SpotPriceRefund, UsagePrice, ZaptecToken

logger = logging.getLogger("django")


def create_post_save_handler(model_name):
    def handler(sender, instance, created, **kwargs):
        if created:
            logger.info(f"Created {model_name} {instance}")
        else:
            logger.info(f"Updated {model_name} {instance}")

    return handler


def create_post_delete_handler(model_name):
    def handler(sender, instance, **kwargs):
        logger.info(f"Deleted {model_name} {instance}")

    return handler


models = [ChargingSession, CostDetails, EnergyDetails, GridPrice, SpotPrice, SpotPriceRefund, UsagePrice, ZaptecToken]
for model in models:
    class_name = model.__name__
    post_save.connect(create_post_save_handler(class_name), sender=model)
    post_delete.connect(create_post_delete_handler(class_name), sender=model)

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from app_Transactions.models import Wallet


@receiver(post_save, sender=User)
def create_user_handler(sender, instance, **kwargs):
    if kwargs['created']:
        Wallet.objects.create(user=instance)

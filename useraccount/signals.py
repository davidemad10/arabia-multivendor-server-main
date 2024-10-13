from company.models import Company
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from stats.models import Stats
from wallet.models import User, Wallet


class ParentWalletNotFoundError(Exception):
    pass


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Stats.objects.get_or_create(name="user stats", show=True)

        if instance.parent_id is None:
            Wallet.objects.create(user=instance, balance=0)

        else:
            try:
                parent_manager_wallet = Wallet.objects.get(user=instance.parent)
                instance.wallet = parent_manager_wallet
                instance.save(update_fields=["wallet"])
            except ObjectDoesNotExist:
                raise ParentWalletNotFoundError("Parent's wallet does not exist.")


@receiver(post_save, sender=User)
def create_company_from_user(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            company_instance, _ = Company.objects.get_or_create(
                user=instance,
                defaults={
                    "name": instance.full_name,
                    "email": instance.email,
                    "phone": instance.phone,
                    "address": instance.shipping_address,
                },
            )

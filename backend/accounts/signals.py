from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile

@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    profile, _ = Profile.objects.get_or_create(user=instance)

    if instance.user_role == 'CITIZEN':
        profile.name = f"{instance.first_name} {instance.last_name}".strip()
    else:  # ORGANIZATION
        profile.name = getattr(instance, 'name', '')

    profile.save()

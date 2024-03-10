from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

#create user profile for each registered user
#when a user is saved send signal witch will be 
#received by receiver
#and this receiver is this create profile function
#witch takes all of the arguments that post_save signal paste to it
#and those are: sender, instance, created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
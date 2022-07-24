from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.mail import  send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Profile

# @receiver(post_save,sender=Profile)
def createProfile(sender,instance,created,**kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )
        subject ='Welcome to Persian-dev.info '
        message = 'we are glade  you are here 😍👌 Thanks dear Friend.'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )

def profileUpdate(sender,instance,created,**kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email =profile.email
        user.save()

def deleteUser(sender,instance,**kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

post_save.connect(createProfile,sender=User)
post_save.connect(profileUpdate,sender=Profile)
post_delete.connect(deleteUser,sender=Profile)
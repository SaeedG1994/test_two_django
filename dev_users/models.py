from django.contrib.auth.models import User
from django.db import models
import uuid
# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=500,null=True,blank=True)
    username = models.CharField(max_length=200,null=True,blank=True)
    short_bio = models.CharField(max_length=200,null=True,blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True,blank=True)
    profile_image = models.ImageField(blank=True,upload_to='profile/',default="profile/user-default.png")
    social_gitHub = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_Linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_Website = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['created']

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return  url




class Skill(models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    description = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True)
    recipient = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name="messages")
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    is_read = models.BooleanField(default=False,null=True)
    body = models.TextField()
    created =models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read','created']

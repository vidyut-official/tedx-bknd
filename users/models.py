from django.db import models


from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(models.Model):
    USER_TYPE = [
        ("Amrita","amrita"),
        ("Others","others")
        
    ]
    USER_ROLE = [
        ("Registration","resgistration"),
        ("Finance","finance"),
        ("Participant", "participant"),
    ]
    username = models.CharField(max_length=100,unique=False,blank=False,null=False)
    user_type = models.CharField(max_length=20,choices=USER_TYPE,default="others",blank=False)
    user_role = models.CharField(max_length=20, choices=USER_ROLE,default="participant")



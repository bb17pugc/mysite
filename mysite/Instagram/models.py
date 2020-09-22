from django.db import models
from django.core.validators import validate_email
from django.core.validators import RegexValidator
import django.dispatch
from time import gmtime, strftime 
from datetime import datetime
from django.db import models 
from django.db.models import Model
from django_mysql.models import ListCharField
from django.db.models import CharField, Model
class Post(models.Model):
        id = models.AutoField
        Title = models.TextField(default='null')
        Description = models.TextField( default='null')
        Image = models.ImageField(upload_to='posts/%y/%m/%d/%H/%m/%S/',default='images/dummy.png')
        Photos = models.JSONField(default='null')
        Vedio = models.TextField(default='null')
        Type=models.TextField(default='null')
        User = models.ForeignKey('User' , on_delete=models.CASCADE )
        DateTime = models.DateTimeField(default=datetime.now, blank=True)
        
class PostDetails(models.Model):
        post = models.ForeignKey('Post' , on_delete=models.CASCADE , related_name='subsciber_user')
        comments=models.TextField(default='null')
        likes=models.TextField(default='null')
        


class Subscriber(models.Model):
        id = models.AutoField
        SubscriberUser = models.ForeignKey('User' , on_delete=models.CASCADE , related_name='subsciber_user')
        SubscribedUser = models.ForeignKey('User' , on_delete=models.CASCADE ,  related_name='subscibed_user')
        
class Seens(models.Model):
        id = models.AutoField
        SeenUser = models.ForeignKey('User' , on_delete=models.CASCADE , default=0 , related_name='seen_user')
        SeenPost = models.ForeignKey('Post' , on_delete=models.CASCADE , default=0 , related_name='seen_post')
        
class Likes(models.Model):
        id = models.AutoField
        LikerUser = models.ForeignKey('User' , on_delete=models.CASCADE , default=0 , related_name='liker_user')
        LikedPost = models.ForeignKey('Post' , on_delete=models.CASCADE , default=0 , related_name='liked_post')


class Comments(models.Model):
        id = models.AutoField
        Description = models.TextField( default='null')
        Status = models.TextField( default='sent')
        SeenUsers = ListCharField(
        base_field=CharField(max_length=10),
        size=6,
        max_length=(6 * 11)  # 6 * 10 character nominals, plus commas
          )
        User = models.ForeignKey('User' , on_delete=models.CASCADE )
        DateTime = models.DateTimeField(default=datetime.now, blank=True)
        Post = models.ForeignKey('Post' , on_delete=models.CASCADE )
        

class Message(models.Model):
        id = models.AutoField
        Description = models.TextField(max_length =191, default='null')
        Status = models.TextField( default='sent')
        Type = models.TextField( default='text')
        Url = models.TextField( default='null')
        Sender = models.ForeignKey('User' , on_delete=models.CASCADE , related_name="message_sender" )
        Reciever = models.ForeignKey('User' , on_delete=models.CASCADE , related_name="message_reciever" )
        DateTime = models.DateTimeField(default=datetime.now, blank=True)

        
               
    

class User(models.Model):

   
    def validate_email(value):

        try:
            validate_email(value)
            return value
        except validate_email.ValidationError:
            raise ValidationError("Email is not valid")

        if not ".edu" in value:
            raise ValidationError("First name is invalid only use alphbets")
        else:
            return value        

   

    id = models.AutoField
    First_Name = models.CharField(max_length=30,validators=[RegexValidator(regex='^[a-zA-Z]*$',message='First name must be Alphanumeric',code='invalid_firstname'),] , default='noname' )
    Last_Name = models.CharField(max_length=30,validators=[RegexValidator(regex='^[a-zA-Z]*$',message='Last name must be Alphanumeric',code='invalid_lastname'),] , default='noname' )
    
    Email = models.CharField(max_length=200,validators=[RegexValidator(regex='^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$',message='Email must be valid',code='invalid_email'),] , default='noname' )
    Username = models.CharField(max_length=200 , default='noname' )
    
    Password = models.CharField(max_length=256)
    Role = models.CharField(max_length=256 , default='user' )
    Status = models.BooleanField(default=False)
    OfflineTime = models.DateTimeField(default=datetime.now, blank=True)
    
    Is_Email_Verified = models.BooleanField(default=False)
    Gender = models.CharField(max_length=256 , default='null' )
    image = models.TextField(default='/media/images/dummy.png')
    

@django.dispatch.receiver(models.signals.post_init, sender=User)
def set_default_loremipsum_initials(sender, instance, *args, **kwargs):
    instance.Username = instance.Email.split("@")[0]   

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class myUser(AbstractUser):
    name = models.CharField(max_length=200, null= True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField( null=True)
    image = models.ImageField(null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
class Location(models.Model):
    user = models.ForeignKey(myUser, on_delete= models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    address = models.TextField()
    
    def __str__(self):
        return f'{self.name}-{self.address}'
        
    
class Participant(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f'{self.email} - {self.name}'
    
class Speaker(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.CASCADE,  null=True, blank=True)
    name = models.CharField(max_length=200)
    proffession = models.CharField(max_length=200, null=True) 
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    meetup_name = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='speaker_img')
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.name}'



class Meetup(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.CASCADE, blank=True, null=True)
    organizer_email = models.EmailField(max_length=254, null=True)
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='image')
    location_name = models.CharField( max_length=50, blank=True,null=True)
    location_address = models.TextField(blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    participant =models.ManyToManyField(Participant, blank=True)
    meetup_speakers =models.ManyToManyField(Speaker, blank=True)
    activate = models.BooleanField(default=True)
    meetup_time = models.DateTimeField(auto_now_add=True)
    meetup_date = models.DateField(blank=True, null=True)
    meetup_endtime = models.TimeField()
    from_date = models.DateField()
    to_date = models.DateField()
    
    def __str__(self):
        return f'{self.title}'

    
    
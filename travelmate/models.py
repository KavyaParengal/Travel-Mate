from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Destination(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='destinations/')
    description = models.TextField()

    def __str__(self):
        return self.name

class TouristPlace(models.Model):
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE,related_name='places')
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='places/')
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True, null=True, default="Unknown")
    google_map_link = models.URLField()
    rating = models.DecimalField(max_digits=2,decimal_places=1,default=0)
    rating_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Restaurant(models.Model):
    touristplace = models.ForeignKey(TouristPlace, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='restaurants/')
    rating = models.FloatField()
    rating_count = models.IntegerField()
    price_range = models.CharField(max_length=50)
    location = models.TextField()
    google_map_link = models.URLField()
    is_open = models.BooleanField(default=True)
    closing_time = models.CharField(max_length=20,blank=True,null=True)

    def __str__(self):
        return self.name
    
class Hotel(models.Model):
    touristplace = models.ForeignKey(TouristPlace,on_delete=models.CASCADE,related_name='hotels')
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='hotels/')
    rating = models.FloatField()
    rating_count = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10,decimal_places=2)
    location = models.TextField()
    adults = models.IntegerField(default=2)
    children = models.IntegerField(default=0)
    available_rooms = models.IntegerField(default=1)
    check_in = models.CharField(max_length=20)
    check_out = models.CharField(max_length=20)
    google_map_link = models.URLField()

    def __str__(self):
        return self.name
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Package(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='packages/')
    duration = models.CharField(max_length=100)
    travel_date = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_recommended = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
class Booking(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    package = models.ForeignKey(Package,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('worker', 'Worker'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_female = models.BooleanField(default=False)
    nid = models.CharField(max_length=20, blank=True)  # hidden, admin only
    nid_image = models.ImageField(upload_to='nid/', blank=True, null=True)  # hidden, admin only
    is_verified = models.BooleanField(default=False)  # this is what users SEE
    def __str__(self):
        return self.user.username

class WorkerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.IntegerField(default=0)
    pricing = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    completed_jobs = models.IntegerField(default=0)
    rating = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ]
    )

    def __str__(self):
        return self.user.username
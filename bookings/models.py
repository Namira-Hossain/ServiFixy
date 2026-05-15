from django.db import models
from accounts.models import UserProfile, WorkerProfile
from services.models import Service

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    final_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.customer} booked {self.service}"

class Rating(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(UserProfile, related_name='given_ratings', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_ratings', on_delete=models.CASCADE)
    score = models.IntegerField(default=5)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.reviewer} rated {self.receiver} - {self.score}/5"

class Discount(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_first_booking = models.BooleanField(default=True)
    discount_percent = models.IntegerField(default=10)

    def __str__(self):
        return f"Discount for {self.customer}"
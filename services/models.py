from django.db import models
from accounts.models import WorkerProfile

class Category(models.Model):
    name = models.CharField(max_length=100)

    def _str_(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    service_image = models.ImageField(upload_to='services/', blank=True, null=True)

    def _str_(self):
        return self.title

class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio/')

    def _str_(self):
        return f"Image for {self.service.title}"
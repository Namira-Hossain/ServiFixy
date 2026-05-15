from django.contrib import admin
from .models import Booking, Rating, Discount

admin.site.register(Booking)
admin.site.register(Rating)
admin.site.register(Discount)
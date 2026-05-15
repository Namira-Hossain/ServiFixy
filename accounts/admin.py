from django.contrib import admin
from .models import UserProfile, WorkerProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'is_verified']
    readonly_fields = ['nid', 'nid_image']

admin.site.register(WorkerProfile)

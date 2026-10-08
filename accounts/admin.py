from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'user_type', 'created_at')
    list_filter = ('user_type',)
    search_fields = ('user__username', 'full_name', 'location')

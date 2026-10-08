from django.contrib import admin
from .models import Category, Campaign

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'status', 'goal_amount', 'current_amount', 'start_date', 'end_date')
    list_filter = ('status', 'category')
    search_fields = ('title', 'short_description', 'description')

from .models import CampaignUpdate

@admin.register(CampaignUpdate)
class CampaignUpdateAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'title', 'created_at')
    list_filter = ('campaign',)
    search_fields = ('title', 'content')

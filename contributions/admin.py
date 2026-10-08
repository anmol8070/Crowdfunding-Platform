from django.contrib import admin
from .models import Contribution

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('transaction_reference', 'contributor', 'campaign', 'amount', 'status', 'created_at')
    list_filter = ('status', 'campaign')
    search_fields = ('transaction_reference', 'contributor__username', 'campaign__title')

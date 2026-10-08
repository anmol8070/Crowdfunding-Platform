from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from campaigns.models import Campaign
import uuid

class Contribution(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gt=0), name='contribution_amount_gt_0')
        ]
        
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    )
    contributor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    transaction_reference = models.CharField(max_length=100, unique=True, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.transaction_reference:
            self.transaction_reference = f"BW-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.contributor.username} -> {self.campaign.title} (${self.amount})"

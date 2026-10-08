import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

def append_to_file(path, content):
    with open(path, 'a', encoding='utf-8') as f:
        f.write('\n' + content.strip() + '\n')

def replace_in_file(path, old, new):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.replace(old, new))

# 1. Update urls.py
replace_in_file('backerwave/urls.py', "path('campaigns/', include('campaigns.urls')),", "path('campaigns/', include('campaigns.urls')),\n    path('contributions/', include('contributions.urls')),")

# 2. Add CampaignUpdate to campaigns/models.py
campaign_update_model = """
class CampaignUpdate(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='campaign_updates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Update for {self.campaign.title}: {self.title}"
"""
append_to_file('campaigns/models.py', campaign_update_model)

# 3. Add to campaigns/admin.py
campaign_update_admin = """
from .models import CampaignUpdate

@admin.register(CampaignUpdate)
class CampaignUpdateAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'title', 'created_at')
    list_filter = ('campaign',)
    search_fields = ('title', 'content')
"""
append_to_file('campaigns/admin.py', campaign_update_admin)

# 4. Add forms to campaigns/forms.py
campaign_update_form = """
from .models import CampaignUpdate

class CampaignUpdateForm(forms.ModelForm):
    class Meta:
        model = CampaignUpdate
        fields = ['title', 'content', 'image']
"""
append_to_file('campaigns/forms.py', campaign_update_form)

# 5. Add views to campaigns/views.py for dashboard & updates
replace_in_file('campaigns/views.py', 
    "'total_contributors': 0, # Placeholder for Phase 3", 
    "'total_contributors': sum(c.contributions.filter(status='SUCCESS').values('contributor').distinct().count() for c in campaigns),\n        'recent_contributions': [contrib for c in campaigns for contrib in c.contributions.filter(status='SUCCESS').order_by('-created_at')[:5]][:5],")

campaigns_new_views = """
@login_required
def campaign_contributors(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    if campaign.creator != request.user:
        messages.error(request, 'You can only view contributors for your own campaigns.')
        return redirect('campaigns:my_campaigns')
    
    contributions = campaign.contributions.filter(status='SUCCESS').order_by('-created_at')
    return render(request, 'campaigns/contributors.html', {'campaign': campaign, 'contributions': contributions})

@login_required
def campaign_update_create(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    if campaign.creator != request.user:
        messages.error(request, 'Only the campaign owner can post updates.')
        return redirect('campaigns:detail', slug=slug)
        
    if request.method == 'POST':
        form = CampaignUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            update.campaign = campaign
            update.save()
            messages.success(request, 'Campaign update published.')
            return redirect('campaigns:detail', slug=slug)
    else:
        form = CampaignUpdateForm()
    return render(request, 'campaigns/update_form.html', {'form': form, 'campaign': campaign})
"""
append_to_file('campaigns/views.py', campaigns_new_views)

# 6. Add urls to campaigns/urls.py
replace_in_file('campaigns/urls.py', 
    "path('<slug:slug>/edit/', views.campaign_edit, name='edit'),",
    "path('<slug:slug>/edit/', views.campaign_edit, name='edit'),\n    path('<slug:slug>/contributors/', views.campaign_contributors, name='contributors'),\n    path('<slug:slug>/updates/create/', views.campaign_update_create, name='update_create'),")

# 7. Create Contributions app models
contributions_models = """
from django.db import models
from django.contrib.auth.models import User
from campaigns.models import Campaign
import uuid

class Contribution(models.Model):
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
"""
write_file('contributions/models.py', contributions_models)

# 8. Contributions Admin
contributions_admin = """
from django.contrib import admin
from .models import Contribution

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('transaction_reference', 'contributor', 'campaign', 'amount', 'status', 'created_at')
    list_filter = ('status', 'campaign')
    search_fields = ('transaction_reference', 'contributor__username', 'campaign__title')
"""
write_file('contributions/admin.py', contributions_admin)

# 9. Contributions Forms
contributions_forms = """
from django import forms
from .models import Contribution

class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['amount', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional message to the creator'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount
"""
write_file('contributions/forms.py', contributions_forms)

# 10. Contributions URLs
contributions_urls = """
from django.urls import path
from . import views

app_name = 'contributions'

urlpatterns = [
    path('dashboard/', views.contributor_dashboard, name='dashboard'),
    path('history/', views.contribution_list, name='list'),
    path('<int:id>/', views.contribution_detail, name='detail'),
    path('<int:id>/receipt/', views.contribution_receipt, name='receipt'),
    path('support/<slug:campaign_slug>/', views.support_campaign, name='support'),
    path('review/<int:id>/', views.review_contribution, name='review'),
    path('success/<int:id>/', views.contribution_success, name='success'),
]
"""
write_file('contributions/urls.py', contributions_urls)

# 11. Contributions Views (Atomic transactions!)
contributions_views = """
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from campaigns.models import Campaign
from .models import Contribution
from .forms import ContributionForm

@login_required
def support_campaign(request, campaign_slug):
    campaign = get_object_or_404(Campaign, slug=campaign_slug)
    
    if campaign.status != 'ACTIVE':
        messages.error(request, 'This campaign is not active and cannot receive contributions.')
        return redirect('campaigns:detail', slug=campaign_slug)
        
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.contributor = request.user
            contribution.campaign = campaign
            contribution.status = 'PENDING'
            contribution.save()
            return redirect('contributions:review', id=contribution.id)
    else:
        form = ContributionForm()
        
    return render(request, 'contributions/support.html', {'form': form, 'campaign': campaign})

@login_required
def review_contribution(request, id):
    contribution = get_object_or_404(Contribution, id=id, contributor=request.user, status='PENDING')
    
    if request.method == 'POST':
        # Simulate payment processing safely
        try:
            with transaction.atomic():
                # Lock campaign row
                campaign = Campaign.objects.select_for_update().get(id=contribution.campaign.id)
                
                if campaign.status != 'ACTIVE':
                    contribution.status = 'FAILED'
                    contribution.save()
                    messages.error(request, 'Campaign is no longer active.')
                    return redirect('campaigns:detail', slug=campaign.slug)
                    
                contribution.status = 'SUCCESS'
                contribution.save()
                
                # Update campaign totals safely
                campaign.current_amount += contribution.amount
                if campaign.current_amount >= campaign.goal_amount:
                    campaign.status = 'COMPLETED'
                campaign.save()
                
                messages.success(request, 'Contribution successful!')
                return redirect('contributions:success', id=contribution.id)
        except Exception as e:
            messages.error(request, 'An error occurred processing your contribution.')
            return redirect('contributions:list')
            
    return render(request, 'contributions/review.html', {'contribution': contribution})

@login_required
def contribution_success(request, id):
    contribution = get_object_or_404(Contribution, id=id, contributor=request.user, status='SUCCESS')
    return render(request, 'contributions/success.html', {'contribution': contribution})

@login_required
def contribution_receipt(request, id):
    contribution = get_object_or_404(Contribution, id=id, contributor=request.user, status='SUCCESS')
    return render(request, 'contributions/receipt.html', {'contribution': contribution})

@login_required
def contribution_list(request):
    contributions = Contribution.objects.filter(contributor=request.user).order_by('-created_at')
    return render(request, 'contributions/list.html', {'contributions': contributions})

@login_required
def contribution_detail(request, id):
    contribution = get_object_or_404(Contribution, id=id, contributor=request.user)
    return render(request, 'contributions/detail.html', {'contribution': contribution})

@login_required
def contributor_dashboard(request):
    contributions = Contribution.objects.filter(contributor=request.user, status='SUCCESS')
    total_amount = contributions.aggregate(Sum('amount'))['amount__sum'] or 0
    supported_campaigns = contributions.values('campaign').distinct().count()
    
    context = {
        'total_contributions': contributions.count(),
        'total_amount': total_amount,
        'supported_campaigns': supported_campaigns,
        'recent_contributions': contributions.order_by('-created_at')[:5]
    }
    return render(request, 'contributions/dashboard.html', context)
"""
write_file('contributions/views.py', contributions_views)

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

# 1. Core Models (Notification, ContactMessage)
core_models = """
from django.db import models
from django.contrib.auth.models import User
from campaigns.models import Campaign

class ContactMessage(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} by {self.name}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    message = models.TextField()
    related_campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user.username}: {self.title}"
"""
write_file('core/models.py', core_models)

# 2. Core Admin
core_admin = """
from django.contrib import admin
from .models import ContactMessage, Notification

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'notification_type')
    search_fields = ('user__username', 'title')
"""
write_file('core/admin.py', core_admin)

# 3. Core Forms
core_forms = """
from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
"""
write_file('core/forms.py', core_forms)

# 4. Campaigns Models update (FavoriteCampaign)
campaign_models_append = """
class FavoriteCampaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'campaign')

    def __str__(self):
        return f"{self.user.username} favorited {self.campaign.title}"
"""
append_to_file('campaigns/models.py', campaign_models_append)

# 5. Core context processor (for unread notifications)
core_cp = """
from .models import Notification

def notifications_processor(request):
    if request.user.is_authenticated:
        return {'unread_notifications_count': Notification.objects.filter(user=request.user, is_read=False).count()}
    return {}
"""
write_file('core/context_processors.py', core_cp)

# Update settings for context processor
replace_in_file('backerwave/settings.py', 
    "'django.contrib.messages.context_processors.messages',", 
    "'django.contrib.messages.context_processors.messages',\n                'core.context_processors.notifications_processor',")

# 6. Core Views Updates (Home stats, About stats, Contact handling, Notifications)
core_views = """
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from campaigns.models import Campaign
from contributions.models import Contribution
from .forms import ContactMessageForm
from .models import Notification
from django.utils import timezone
from datetime import timedelta

def home(request):
    active_campaigns = Campaign.objects.filter(status='ACTIVE')
    featured = active_campaigns.annotate(num_backers=Count('contributions')).order_by('-num_backers')[:3]
    trending = active_campaigns.annotate(raised=Sum('contributions__amount')).order_by('-raised')[:3]
    recent = active_campaigns.order_by('-created_at')[:3]
    ending_soon = active_campaigns.filter(end_date__gte=timezone.now().date(), end_date__lte=timezone.now().date() + timedelta(days=7))[:3]
    
    stats = {
        'total_campaigns': Campaign.objects.count(),
        'active_campaigns': active_campaigns.count(),
        'completed_campaigns': Campaign.objects.filter(status='COMPLETED').count(),
        'total_raised': Contribution.objects.filter(status='SUCCESS').aggregate(Sum('amount'))['amount__sum'] or 0,
        'total_contributors': Contribution.objects.filter(status='SUCCESS').values('contributor').distinct().count(),
    }
    
    return render(request, 'core/home.html', {
        'featured_campaigns': featured,
        'trending_campaigns': trending,
        'recent_campaigns': recent,
        'ending_soon': ending_soon,
        'stats': stats
    })

def about(request):
    stats = {
        'total_campaigns': Campaign.objects.count(),
        'total_raised': Contribution.objects.filter(status='SUCCESS').aggregate(Sum('amount'))['amount__sum'] or 0,
        'total_contributors': Contribution.objects.filter(status='SUCCESS').values('contributor').distinct().count(),
    }
    return render(request, 'core/about.html', {'stats': stats})

def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('core:contact')
    else:
        form = ContactMessageForm()
    return render(request, 'core/contact.html', {'form': form})

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, id):
    notification = get_object_or_404(Notification, id=id, user=request.user)
    notification.is_read = True
    notification.save()
    if notification.related_campaign:
        return redirect('campaigns:detail', slug=notification.related_campaign.slug)
    return redirect('core:notifications')

@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, 'All notifications marked as read.')
    return redirect('core:notifications')
"""
write_file('core/views.py', core_views)

# Core URLs update
core_urls = """
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/read/<int:id>/', views.mark_notification_read, name='mark_read'),
    path('notifications/read-all/', views.mark_all_read, name='mark_all_read'),
]
"""
write_file('core/urls.py', core_urls)

# 7. Update Contributions app to send notifications
replace_in_file('contributions/views.py', "from .models import Contribution", "from .models import Contribution\nfrom core.models import Notification")
replace_in_file('contributions/views.py', 
    "messages.success(request, 'Contribution successful!')", 
    """messages.success(request, 'Contribution successful!')
                # Create notification for contributor
                Notification.objects.create(
                    user=contribution.contributor,
                    notification_type='CONTRIBUTION',
                    title='Contribution Successful',
                    message=f'You successfully backed {campaign.title} for ${contribution.amount}.',
                    related_campaign=campaign
                )
                # Create notification for creator
                Notification.objects.create(
                    user=campaign.creator,
                    notification_type='NEW_BACKER',
                    title='New Backer!',
                    message=f'Someone just backed {campaign.title} for ${contribution.amount}!',
                    related_campaign=campaign
                )
                if campaign.status == 'COMPLETED':
                    Notification.objects.create(
                        user=campaign.creator,
                        notification_type='GOAL_REACHED',
                        title='Goal Reached!',
                        message=f'Congratulations! {campaign.title} reached its funding goal.',
                        related_campaign=campaign
                    )""")

# 8. Update campaigns/views.py for favorites, discovery improvements, and notifications
replace_in_file('campaigns/views.py', "from .models import Campaign, Category", "from .models import Campaign, Category, FavoriteCampaign\nfrom core.models import Notification\nfrom django.core.paginator import Paginator\nfrom django.contrib.auth.models import User")

campaign_list_replacement = """
def campaign_list(request):
    campaigns = Campaign.objects.filter(status='ACTIVE').select_related('creator', 'category')
    
    # Search
    query = request.GET.get('q')
    if query:
        campaigns = campaigns.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        campaigns = campaigns.filter(category__slug=category)
        
    # Min/Max Goal
    min_goal = request.GET.get('min_goal')
    max_goal = request.GET.get('max_goal')
    if min_goal and min_goal.isdigit():
        campaigns = campaigns.filter(goal_amount__gte=min_goal)
    if max_goal and max_goal.isdigit():
        campaigns = campaigns.filter(goal_amount__lte=max_goal)
    
    # Sort
    sort = request.GET.get('sort', '-created_at')
    if sort == '-created_at':
        campaigns = campaigns.order_by('-created_at')
    elif sort == 'created_at':
        campaigns = campaigns.order_by('created_at')
    elif sort == '-current_amount':
        campaigns = campaigns.order_by('-current_amount')
    elif sort == 'end_date':
        campaigns = campaigns.order_by('end_date')
    elif sort == '-goal_amount':
        campaigns = campaigns.order_by('-goal_amount')
        
    categories = Category.objects.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(campaigns, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'campaigns/list.html', {
        'campaigns': page_obj,
        'categories': categories,
        'page_obj': page_obj
    })
"""

# We need to replace the entire campaign_list function
# Let's do it by regex or just rewriting the view file partially.
# Actually, let's just append the new views and we will replace the whole file content to be safe.
"""
Instead of doing risky replacements, I will rewrite `campaigns/views.py` completely but keeping all existing logic.
"""
campaigns_views_full = """
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from core.models import Notification
from .models import Campaign, Category, FavoriteCampaign
from .forms import CampaignForm, CampaignUpdateForm

def campaign_list(request):
    campaigns = Campaign.objects.filter(status='ACTIVE').select_related('creator', 'category')
    
    query = request.GET.get('q')
    if query:
        campaigns = campaigns.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    category = request.GET.get('category')
    if category:
        campaigns = campaigns.filter(category__slug=category)
        
    min_goal = request.GET.get('min_goal')
    max_goal = request.GET.get('max_goal')
    if min_goal and min_goal.isdigit():
        campaigns = campaigns.filter(goal_amount__gte=min_goal)
    if max_goal and max_goal.isdigit():
        campaigns = campaigns.filter(goal_amount__lte=max_goal)
    
    sort = request.GET.get('sort', '-created_at')
    valid_sorts = {
        '-created_at': '-created_at',
        'created_at': 'created_at',
        '-current_amount': '-current_amount',
        'end_date': 'end_date',
        '-goal_amount': '-goal_amount'
    }
    campaigns = campaigns.order_by(valid_sorts.get(sort, '-created_at'))
        
    categories = Category.objects.filter(is_active=True)
    paginator = Paginator(campaigns, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'campaigns/list.html', {
        'page_obj': page_obj,
        'categories': categories,
    })

def campaign_detail(request, slug):
    campaign = get_object_or_404(Campaign.objects.select_related('creator', 'creator__profile', 'category'), slug=slug)
    if campaign.status != 'ACTIVE' and request.user != campaign.creator and not request.user.is_staff:
        messages.error(request, 'Campaign not found or inactive.')
        return redirect('campaigns:list')
        
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = FavoriteCampaign.objects.filter(user=request.user, campaign=campaign).exists()
        
    return render(request, 'campaigns/detail.html', {'campaign': campaign, 'is_favorited': is_favorited})

@login_required
def my_campaigns(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'CREATOR':
        messages.error(request, 'Only creators can access the dashboard.')
        return redirect('core:home')
    
    campaigns = Campaign.objects.filter(creator=request.user).prefetch_related('contributions')
    
    context = {
        'campaigns': campaigns,
        'total_campaigns': campaigns.count(),
        'active_campaigns': campaigns.filter(status='ACTIVE').count(),
        'completed_campaigns': campaigns.filter(status='COMPLETED').count(),
        'total_raised': sum(c.current_amount for c in campaigns),
        'total_contributors': sum(c.contributions.filter(status='SUCCESS').values('contributor').distinct().count() for c in campaigns),
        'recent_contributions': [contrib for c in campaigns for contrib in c.contributions.filter(status='SUCCESS').order_by('-created_at')[:5]][:5],
    }
    return render(request, 'campaigns/my_campaigns.html', context)

@login_required
def campaign_create(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'CREATOR':
        messages.error(request, 'Only creators can create campaigns.')
        return redirect('core:home')

    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.creator = request.user
            campaign.save()
            Notification.objects.create(
                user=request.user,
                notification_type='CAMPAIGN_CREATED',
                title='Campaign Created',
                message=f'Your campaign "{campaign.title}" was created successfully and is in draft.'
            )
            messages.success(request, 'Campaign created successfully!')
            return redirect('campaigns:my_campaigns')
    else:
        form = CampaignForm()
    return render(request, 'campaigns/form.html', {'form': form, 'title': 'Create Campaign'})

@login_required
def campaign_edit(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    if campaign.creator != request.user:
        messages.error(request, 'You can only edit your own campaigns.')
        return redirect('campaigns:my_campaigns')
        
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaign updated successfully!')
            return redirect('campaigns:my_campaigns')
    else:
        form = CampaignForm(instance=campaign)
    return render(request, 'campaigns/form.html', {'form': form, 'title': 'Edit Campaign'})

@login_required
def campaign_delete(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    if campaign.creator != request.user:
        messages.error(request, 'You can only delete your own campaigns.')
        return redirect('campaigns:my_campaigns')
        
    if request.method == 'POST':
        campaign.delete()
        messages.success(request, 'Campaign deleted.')
        return redirect('campaigns:my_campaigns')
    return render(request, 'campaigns/confirm_delete.html', {'campaign': campaign})

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
            
            # Notify followers
            followers = FavoriteCampaign.objects.filter(campaign=campaign)
            for follower in followers:
                Notification.objects.create(
                    user=follower.user,
                    notification_type='CAMPAIGN_UPDATE',
                    title=f'Update on {campaign.title}',
                    message=f'{campaign.creator.username} posted an update: {update.title}',
                    related_campaign=campaign
                )
            
            messages.success(request, 'Campaign update published.')
            return redirect('campaigns:detail', slug=slug)
    else:
        form = CampaignUpdateForm()
    return render(request, 'campaigns/update_form.html', {'form': form, 'campaign': campaign})

@login_required
def toggle_favorite(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    favorite, created = FavoriteCampaign.objects.get_or_create(user=request.user, campaign=campaign)
    if not created:
        favorite.delete()
        messages.success(request, f'Removed {campaign.title} from your favorites.')
    else:
        messages.success(request, f'Added {campaign.title} to your favorites! You will receive updates.')
    return redirect('campaigns:detail', slug=slug)

@login_required
def favorites_list(request):
    favorites = FavoriteCampaign.objects.filter(user=request.user).select_related('campaign')
    return render(request, 'campaigns/favorites.html', {'favorites': favorites})

def creator_profile(request, username):
    creator = get_object_or_404(User.objects.select_related('profile'), username=username)
    if creator.profile.user_type != 'CREATOR':
        messages.error(request, 'Profile not found.')
        return redirect('core:home')
        
    campaigns = Campaign.objects.filter(creator=creator, status='ACTIVE').order_by('-created_at')
    completed = Campaign.objects.filter(creator=creator, status='COMPLETED').count()
    total_raised = Contribution.objects.filter(campaign__creator=creator, status='SUCCESS').aggregate(Sum('amount'))['amount__sum'] or 0
    
    return render(request, 'campaigns/creator_profile.html', {
        'creator': creator,
        'campaigns': campaigns,
        'completed_count': completed,
        'total_raised': total_raised
    })
"""
write_file('campaigns/views.py', campaigns_views_full)

# Add new URLs to campaigns/urls.py
replace_in_file('campaigns/urls.py', 
    "path('<slug:slug>/updates/create/', views.campaign_update_create, name='update_create'),",
    "path('<slug:slug>/updates/create/', views.campaign_update_create, name='update_create'),\n    path('<slug:slug>/favorite/', views.toggle_favorite, name='favorite'),\n    path('favorites/', views.favorites_list, name='favorites'),\n    path('creator/<str:username>/', views.creator_profile, name='creator_profile'),")

# Error pages in backerwave/urls.py
backerwave_urls = """
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('campaigns/', include('campaigns.urls')),
    path('contributions/', include('contributions.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.home' # Simplistic fallback
handler403 = 'core.views.home'
handler500 = 'core.views.home'
"""
write_file('backerwave/urls.py', backerwave_urls)

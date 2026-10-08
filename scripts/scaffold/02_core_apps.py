import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

urls_py = """
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('campaigns/', include('campaigns.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
write_file('backerwave/urls.py', urls_py)

accounts_models = """
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('CONTRIBUTOR', 'Contributor'),
        ('CREATOR', 'Creator'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='CONTRIBUTOR')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
"""
write_file('accounts/models.py', accounts_models)

accounts_admin = """
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'user_type', 'created_at')
    list_filter = ('user_type',)
    search_fields = ('user__username', 'full_name', 'location')
"""
write_file('accounts/admin.py', accounts_admin)

accounts_forms = """
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords don't match")
        return cleaned_data

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'profile_image', 'bio', 'phone', 'location']
"""
write_file('accounts/forms.py', accounts_forms)

accounts_urls = """
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
"""
write_file('accounts/urls.py', accounts_urls)

accounts_views = """
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileUpdateForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(
                user=user, 
                user_type=form.cleaned_data['user_type'],
                full_name=user.username
            )
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):
    profile_obj = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=profile_obj)
    return render(request, 'accounts/edit_profile.html', {'form': form})
"""
write_file('accounts/views.py', accounts_views)

core_urls = """
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
"""
write_file('core/urls.py', core_urls)

core_views = """
from django.shortcuts import render
from campaigns.models import Campaign

def home(request):
    featured_campaigns = Campaign.objects.filter(status='ACTIVE')[:3]
    return render(request, 'core/home.html', {'featured_campaigns': featured_campaigns})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')
"""
write_file('core/views.py', core_views)

campaigns_models = """
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Campaign(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('REJECTED', 'Rejected'),
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='campaigns')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    start_date = models.DateField()
    end_date = models.DateField()
    campaign_image = models.ImageField(upload_to='campaigns/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness
            unique_slug = self.slug
            num = 1
            while Campaign.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{self.slug}-{num}'
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    @property
    def progress_percentage(self):
        if self.goal_amount > 0:
            percentage = (self.current_amount / self.goal_amount) * 100
            return min(percentage, 100)
        return 0

    @property
    def remaining_amount(self):
        rem = self.goal_amount - self.current_amount
        return rem if rem > 0 else 0

    def __str__(self):
        return self.title
"""
write_file('campaigns/models.py', campaigns_models)

campaigns_admin = """
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
"""
write_file('campaigns/admin.py', campaigns_admin)

campaigns_forms = """
from django import forms
from .models import Campaign
from datetime import date

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'short_description', 'description', 'category', 'goal_amount', 'start_date', 'end_date', 'location', 'campaign_image', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        goal = cleaned_data.get('goal_amount')
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if goal and goal <= 0:
            self.add_error('goal_amount', "Goal amount must be greater than zero.")
        if start and end and end <= start:
            self.add_error('end_date', "End date must be after the start date.")
        
        return cleaned_data
"""
write_file('campaigns/forms.py', campaigns_forms)

campaigns_urls = """
from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('', views.campaign_list, name='list'),
    path('my-campaigns/', views.my_campaigns, name='my_campaigns'),
    path('create/', views.campaign_create, name='create'),
    path('<slug:slug>/', views.campaign_detail, name='detail'),
    path('<slug:slug>/edit/', views.campaign_edit, name='edit'),
    path('<slug:slug>/delete/', views.campaign_delete, name='delete'),
]
"""
write_file('campaigns/urls.py', campaigns_urls)

campaigns_views = """
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Campaign, Category
from .forms import CampaignForm

def campaign_list(request):
    campaigns = Campaign.objects.filter(status='ACTIVE')
    
    # Search
    query = request.GET.get('q')
    if query:
        campaigns = campaigns.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Filter
    category = request.GET.get('category')
    if category:
        campaigns = campaigns.filter(category__slug=category)
    
    # Sort
    sort = request.GET.get('sort', '-created_at')
    if sort in ['-created_at', 'end_date', '-current_amount', '-goal_amount']:
        campaigns = campaigns.order_by(sort)
        
    categories = Category.objects.filter(is_active=True)
    return render(request, 'campaigns/list.html', {
        'campaigns': campaigns,
        'categories': categories
    })

def campaign_detail(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    if campaign.status != 'ACTIVE' and request.user != campaign.creator:
        if not request.user.is_staff:
            messages.error(request, 'Campaign not found or inactive.')
            return redirect('campaigns:list')
    return render(request, 'campaigns/detail.html', {'campaign': campaign})

@login_required
def my_campaigns(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'CREATOR':
        messages.error(request, 'Only creators can access the dashboard.')
        return redirect('core:home')
    
    campaigns = Campaign.objects.filter(creator=request.user)
    
    context = {
        'campaigns': campaigns,
        'total_campaigns': campaigns.count(),
        'active_campaigns': campaigns.filter(status='ACTIVE').count(),
        'completed_campaigns': campaigns.filter(status='COMPLETED').count(),
        'total_raised': sum(c.current_amount for c in campaigns),
        'total_contributors': 0, # Placeholder for Phase 3
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
"""
write_file('campaigns/views.py', campaigns_views)

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

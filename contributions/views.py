from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from campaigns.models import Campaign
from .models import Contribution
from core.models import Notification
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
                    )
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

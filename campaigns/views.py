from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from core.models import Notification
from contributions.models import Contribution
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
        'campaigns': page_obj,
        'page_obj': page_obj,
        'categories': categories,
    })

def campaign_detail(request, slug):
    campaign = get_object_or_404(Campaign.objects.select_related('creator', 'creator__profile', 'category'), slug=slug)
    if campaign.status != 'ACTIVE' and request.user != campaign.creator and not request.user.is_staff:
        messages.error(request, 'Campaign not found or inactive.')
        return redirect('campaigns:list')
        
    # Track view
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    
    from .models import CampaignView
    if not CampaignView.objects.filter(campaign=campaign, session_key=session_key).exists():
        CampaignView.objects.create(
            campaign=campaign,
            session_key=session_key,
            user=request.user if request.user.is_authenticated else None
        )
        
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = FavoriteCampaign.objects.filter(user=request.user, campaign=campaign).exists()
        
    comments = campaign.comments.filter(parent__isnull=True).prefetch_related('replies', 'replies__user')
        
    return render(request, 'campaigns/detail.html', {'campaign': campaign, 'is_favorited': is_favorited, 'comments': comments})

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

from .models import CampaignMilestone
from .forms import CampaignMilestoneForm
from django.utils import timezone

@login_required
def milestone_create(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    if request.user != campaign.creator:
        messages.error(request, "Unauthorized access.")
        return redirect('campaigns:detail', slug=slug)
    
    if request.method == 'POST':
        form = CampaignMilestoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.campaign = campaign
            if milestone.status == 'COMPLETED':
                milestone.completed_at = timezone.now()
            milestone.save()
            messages.success(request, "Milestone created.")
            return redirect('campaigns:my_campaigns')
    else:
        form = CampaignMilestoneForm()
    
    return render(request, 'campaigns/milestone_form.html', {'form': form, 'campaign': campaign, 'title': 'Add Milestone'})

@login_required
def milestone_edit(request, slug, pk):
    campaign = get_object_or_404(Campaign, slug=slug)
    milestone = get_object_or_404(CampaignMilestone, pk=pk, campaign=campaign)
    
    if request.user != campaign.creator:
        messages.error(request, "Unauthorized access.")
        return redirect('campaigns:detail', slug=slug)
        
    if request.method == 'POST':
        form = CampaignMilestoneForm(request.POST, instance=milestone)
        if form.is_valid():
            milestone = form.save(commit=False)
            if milestone.status == 'COMPLETED' and not milestone.completed_at:
                milestone.completed_at = timezone.now()
            elif milestone.status == 'PENDING':
                milestone.completed_at = None
            milestone.save()
            messages.success(request, "Milestone updated.")
            return redirect('campaigns:my_campaigns')
    else:
        form = CampaignMilestoneForm(instance=milestone)
        
    return render(request, 'campaigns/milestone_form.html', {'form': form, 'campaign': campaign, 'title': 'Edit Milestone'})

@login_required
def milestone_delete(request, slug, pk):
    campaign = get_object_or_404(Campaign, slug=slug)
    milestone = get_object_or_404(CampaignMilestone, pk=pk, campaign=campaign)
    
    if request.user != campaign.creator:
        messages.error(request, "Unauthorized access.")
        return redirect('campaigns:detail', slug=slug)
        
    if request.method == 'POST':
        milestone.delete()
        messages.success(request, "Milestone deleted.")
        return redirect('campaigns:my_campaigns')
        
    return render(request, 'campaigns/milestone_confirm_delete.html', {'milestone': milestone, 'campaign': campaign})

from .models import CampaignComment, CommentReport
from .forms import CampaignCommentForm, CommentReportForm

@login_required
def comment_add(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    if request.method == 'POST':
        form = CampaignCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.campaign = campaign
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment was added successfully.')
    return redirect('campaigns:detail', slug=slug)

@login_required
def comment_reply(request, pk):
    parent = get_object_or_404(CampaignComment, pk=pk)
    if request.method == 'POST':
        form = CampaignCommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.campaign = parent.campaign
            reply.user = request.user
            reply.parent = parent
            reply.save()
            
            # Notify parent comment author
            if parent.user != request.user:
                Notification.objects.create(
                    user=parent.user,
                    notification_type='COMMENT_REPLY',
                    title='New Reply',
                    message=f'{request.user.username} replied to your comment on {parent.campaign.title}',
                    related_campaign=parent.campaign
                )
            messages.success(request, 'Your reply was added successfully.')
    return redirect('campaigns:detail', slug=parent.campaign.slug)

@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(CampaignComment, pk=pk)
    if comment.user != request.user:
        messages.error(request, 'You can only edit your own comments.')
        return redirect('campaigns:detail', slug=comment.campaign.slug)
        
    if request.method == 'POST':
        form = CampaignCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment was updated.')
            return redirect('campaigns:detail', slug=comment.campaign.slug)
    else:
        form = CampaignCommentForm(instance=comment)
        
    return render(request, 'campaigns/comment_form.html', {'form': form, 'comment': comment, 'campaign': comment.campaign})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(CampaignComment, pk=pk)
    if comment.user != request.user:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('campaigns:detail', slug=comment.campaign.slug)
        
    if request.method == 'POST':
        campaign_slug = comment.campaign.slug
        comment.delete()
        messages.success(request, 'Your comment was deleted.')
        return redirect('campaigns:detail', slug=campaign_slug)
        
    return render(request, 'campaigns/comment_confirm_delete.html', {'comment': comment, 'campaign': comment.campaign})

@login_required
def comment_pin(request, pk):
    comment = get_object_or_404(CampaignComment, pk=pk)
    if comment.campaign.creator != request.user:
        messages.error(request, 'Only the creator can pin comments.')
        return redirect('campaigns:detail', slug=comment.campaign.slug)
        
    if request.method == 'POST':
        comment.is_pinned = not comment.is_pinned
        comment.save()
        status = 'pinned' if comment.is_pinned else 'unpinned'
        messages.success(request, f'Comment {status} successfully.')
        
    return redirect('campaigns:detail', slug=comment.campaign.slug)

@login_required
def comment_report(request, pk):
    comment = get_object_or_404(CampaignComment, pk=pk)
    if request.method == 'POST':
        form = CommentReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.comment = comment
            report.user = request.user
            try:
                report.save()
                messages.success(request, 'Comment reported successfully.')
            except:
                messages.error(request, 'You have already reported this comment.')
            return redirect('campaigns:detail', slug=comment.campaign.slug)
    else:
        form = CommentReportForm()
        
    return render(request, 'campaigns/comment_report_form.html', {'form': form, 'comment': comment, 'campaign': comment.campaign})

from django.db.models.functions import TruncDate
from django.db.models import Count
import json

@login_required
def campaign_analytics(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    if request.user != campaign.creator and not request.user.is_staff:
        messages.error(request, 'Unauthorized access.')
        return redirect('campaigns:detail', slug=slug)

    total_views = campaign.views.count()
    unique_visitors = campaign.views.values('session_key').distinct().count()
    
    success_contributions = campaign.contributions.filter(status='SUCCESS')
    total_raised = success_contributions.aggregate(Sum('amount'))['amount__sum'] or 0
    contributors_count = success_contributions.values('contributor').distinct().count()
    
    avg_contribution = float(total_raised) / success_contributions.count() if success_contributions.exists() else 0
    conversion_rate = (success_contributions.count() / unique_visitors * 100) if unique_visitors > 0 else 0
    
    daily_raised = success_contributions.annotate(date=TruncDate('created_at')).values('date').annotate(total=Sum('amount')).order_by('date')
    daily_contribs = success_contributions.annotate(date=TruncDate('created_at')).values('date').annotate(count=Count('id')).order_by('date')
    
    dates_raised = [obj['date'].strftime('%Y-%m-%d') for obj in daily_raised]
    amounts_raised = [float(obj['total']) for obj in daily_raised]
    
    dates_contribs = [obj['date'].strftime('%Y-%m-%d') for obj in daily_contribs]
    counts_contribs = [obj['count'] for obj in daily_contribs]

    context = {
        'campaign': campaign,
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'total_raised': total_raised,
        'contributors_count': contributors_count,
        'avg_contribution': avg_contribution,
        'conversion_rate': conversion_rate,
        'chart_dates_raised': json.dumps(dates_raised),
        'chart_amounts_raised': json.dumps(amounts_raised),
        'chart_dates_contribs': json.dumps(dates_contribs),
        'chart_counts_contribs': json.dumps(counts_contribs),
    }
    return render(request, 'campaigns/analytics.html', context)

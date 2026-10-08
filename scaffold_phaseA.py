import os

def append_to_file(path, content):
    with open(path, 'a', encoding='utf-8') as f:
        f.write('\n' + content.strip() + '\n')

def replace_in_file(path, old, new):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.replace(old, new))

# 1. Add CampaignMilestone Model
models_addition = """
class CampaignMilestone(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    )
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    order = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        constraints = [
            models.CheckConstraint(check=models.Q(target_amount__gt=0), name='milestone_target_gt_0')
        ]

    def __str__(self):
        return f"{self.campaign.title} - {self.title}"
"""
append_to_file('campaigns/models.py', models_addition)

# 2. Add Milestone Forms
forms_addition = """
from .models import CampaignMilestone

class CampaignMilestoneForm(forms.ModelForm):
    class Meta:
        model = CampaignMilestone
        fields = ['title', 'description', 'target_amount', 'order', 'status']
"""
append_to_file('campaigns/forms.py', forms_addition)

# 3. Add Milestone Views (in campaigns/views.py)
# We'll just add the necessary views: milestone_create, milestone_edit, milestone_delete, milestone_complete
views_addition = """
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
"""
append_to_file('campaigns/views.py', views_addition)

# 4. Add to urls.py
urls_addition = """
    path('<slug:slug>/milestones/create/', views.milestone_create, name='milestone_create'),
    path('<slug:slug>/milestones/<int:pk>/edit/', views.milestone_edit, name='milestone_edit'),
    path('<slug:slug>/milestones/<int:pk>/delete/', views.milestone_delete, name='milestone_delete'),
"""
replace_in_file('campaigns/urls.py', 
    "path('<slug:slug>/favorite/', views.favorite_toggle, name='favorite'),",
    "path('<slug:slug>/favorite/', views.favorite_toggle, name='favorite'),\n" + urls_addition)

# 5. Add to detail.html (Timeline component)
timeline_html = """
                <hr class="border-subtle my-5">
                <h4 class="fw-bold mb-4">Project Milestones</h4>
                <div class="position-relative ps-4 border-start border-subtle border-2 ms-3">
                    {% for milestone in campaign.milestones.all %}
                        <div class="mb-4 position-relative">
                            <div class="position-absolute translate-middle rounded-circle border border-2 border-white 
                                {% if milestone.status == 'COMPLETED' %}bg-success{% else %}bg-secondary{% endif %}" 
                                style="width: 16px; height: 16px; left: -16px; top: 8px;"></div>
                            <h5 class="fw-bold mb-1 {% if milestone.status == 'COMPLETED' %}text-success{% endif %}">
                                {{ milestone.title }} <span class="badge bg-light text-muted ms-2">${{ milestone.target_amount }}</span>
                            </h5>
                            <p class="text-muted mb-0 text-small">{{ milestone.description }}</p>
                            {% if milestone.status == 'COMPLETED' %}
                                <div class="text-success text-caption fw-medium mt-1"><i class="bi bi-check-circle me-1"></i> Completed on {{ milestone.completed_at|date:"M d, Y" }}</div>
                            {% endif %}
                        </div>
                    {% empty %}
                        <p class="text-muted mb-0">No milestones have been set for this project yet.</p>
                    {% endfor %}
                </div>
"""
replace_in_file('templates/campaigns/detail.html',
    "<!-- Creator Card -->",
    timeline_html + "\n                    <!-- Creator Card -->")

# 6. Add milestone form template
milestone_form_html = """
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="container py-5 max-w-700" style="max-width: 600px;">
    <h2 class="fw-bold mb-4">{{ title }}</h2>
    <form method="post" class="card border-subtle shadow-sm rounded-4 p-4 p-lg-5">
        {% csrf_token %}
        {{ form.as_p }}
        <div class="d-flex gap-2 mt-4">
            <a href="{% url 'campaigns:my_campaigns' %}" class="btn btn-light w-100 fw-medium">Cancel</a>
            <button type="submit" class="btn btn-primary w-100 fw-bold">Save Milestone</button>
        </div>
    </form>
</div>
{% endblock %}
"""
with open('templates/campaigns/milestone_form.html', 'w', encoding='utf-8') as f:
    f.write(milestone_form_html.strip() + '\n')

# 7. Add milestone delete template
milestone_delete_html = """
{% extends 'base.html' %}
{% block title %}Delete Milestone{% endblock %}

{% block content %}
<div class="container py-5 max-w-700 text-center" style="max-width: 600px;">
    <h2 class="fw-bold mb-4 text-danger">Delete Milestone</h2>
    <p class="text-muted">Are you sure you want to delete the milestone <strong>{{ milestone.title }}</strong>?</p>
    <form method="post" class="mt-4">
        {% csrf_token %}
        <div class="d-flex justify-content-center gap-3">
            <a href="{% url 'campaigns:my_campaigns' %}" class="btn btn-light px-4 fw-medium">Cancel</a>
            <button type="submit" class="btn btn-danger px-4 fw-bold">Yes, Delete</button>
        </div>
    </form>
</div>
{% endblock %}
"""
with open('templates/campaigns/milestone_confirm_delete.html', 'w', encoding='utf-8') as f:
    f.write(milestone_delete_html.strip() + '\n')

# 8. Add tests for Milestones
tests_addition = """
    def test_create_milestone_creator(self):
        self.client.login(username='creator', password='password123')
        response = self.client.post(reverse('campaigns:milestone_create', args=[self.campaign.slug]), {
            'title': 'Test Milestone',
            'description': 'Desc',
            'target_amount': 500,
            'order': 1,
            'status': 'PENDING'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.campaign.milestones.filter(title='Test Milestone').exists())

    def test_create_milestone_unauthorized(self):
        self.client.login(username='contributor', password='password123')
        response = self.client.post(reverse('campaigns:milestone_create', args=[self.campaign.slug]), {
            'title': 'Test Milestone',
            'description': 'Desc',
            'target_amount': 500,
            'order': 1,
            'status': 'PENDING'
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.campaign.milestones.filter(title='Test Milestone').exists())
"""
append_to_file('campaigns/tests.py', tests_addition)

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

from .models import CampaignUpdate

class CampaignUpdateForm(forms.ModelForm):
    class Meta:
        model = CampaignUpdate
        fields = ['title', 'content', 'image']

from .models import CampaignMilestone

class CampaignMilestoneForm(forms.ModelForm):
    class Meta:
        model = CampaignMilestone
        fields = ['title', 'description', 'target_amount', 'order', 'status']

from .models import CampaignComment, CommentReport

class CampaignCommentForm(forms.ModelForm):
    class Meta:
        model = CampaignComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'})
        }

class CommentReportForm(forms.ModelForm):
    class Meta:
        model = CommentReport
        fields = ['reason']
        widgets = {
            'reason': forms.TextInput(attrs={'placeholder': 'Reason for reporting'})
        }

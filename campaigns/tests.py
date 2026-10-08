from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Category, Campaign
from datetime import date, timedelta

class CampaignTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.creator_user = User.objects.create_user(username='creator', password='password123')
        Profile.objects.create(user=self.creator_user, user_type='CREATOR')
        
        self.contributor_user = User.objects.create_user(username='contributor', password='password123')
        Profile.objects.create(user=self.contributor_user, user_type='CONTRIBUTOR')

        self.category = Category.objects.create(name='Tech')
        
        self.campaign = Campaign.objects.create(
            creator=self.creator_user,
            title='Test Campaign',
            category=self.category,
            short_description='Short',
            description='Long',
            goal_amount=1000,
            current_amount=250,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            status='ACTIVE'
        )

    def test_progress_calculation(self):
        self.assertEqual(self.campaign.progress_percentage, 25.0)
        self.assertEqual(self.campaign.remaining_amount, 750)

    def test_campaign_list(self):
        response = self.client.get(reverse('campaigns:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Campaign')

    def test_campaign_detail(self):
        response = self.client.get(reverse('campaigns:detail', args=[self.campaign.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Campaign')

    def test_campaign_search(self):
        response = self.client.get(reverse('campaigns:list') + '?q=Test')
        self.assertContains(response, 'Test Campaign')
        response2 = self.client.get(reverse('campaigns:list') + '?q=RandomWord')
        self.assertNotContains(response2, 'Test Campaign')

    def test_campaign_filter(self):
        response = self.client.get(reverse('campaigns:list') + f'?category={self.category.slug}')
        self.assertContains(response, 'Test Campaign')

    def test_create_campaign_auth(self):
        response = self.client.get(reverse('campaigns:create'))
        self.assertEqual(response.status_code, 302)

    def test_create_campaign_contributor(self):
        self.client.login(username='contributor', password='password123')
        response = self.client.get(reverse('campaigns:create'))
        self.assertEqual(response.status_code, 302) # Redirects home

    def test_create_campaign_creator(self):
        self.client.login(username='creator', password='password123')
        response = self.client.get(reverse('campaigns:create'))
        self.assertEqual(response.status_code, 200)

        post_data = {
            'title': 'New Campaign',
            'category': self.category.id,
            'short_description': 'Short',
            'description': 'Long description',
            'goal_amount': 5000,
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=10),
            'status': 'DRAFT'
        }
        resp = self.client.post(reverse('campaigns:create'), post_data)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Campaign.objects.filter(title='New Campaign').exists())

    def test_edit_campaign(self):
        self.client.login(username='creator', password='password123')
        response = self.client.post(reverse('campaigns:edit', args=[self.campaign.slug]), {
            'title': 'Updated Title',
            'category': self.category.id,
            'short_description': 'Short',
            'description': 'Long',
            'goal_amount': 1000,
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=30),
            'status': 'ACTIVE'
        })
        self.assertEqual(response.status_code, 302)
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.title, 'Updated Title')

    def test_edit_campaign_unauthorized(self):
        self.client.login(username='contributor', password='password123')
        response = self.client.post(reverse('campaigns:edit', args=[self.campaign.slug]), {
            'title': 'Hacked Title',
        })
        self.assertEqual(response.status_code, 302)
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.title, 'Test Campaign')

    def test_delete_campaign(self):
        self.client.login(username='creator', password='password123')
        response = self.client.post(reverse('campaigns:delete', args=[self.campaign.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Campaign.objects.filter(id=self.campaign.id).exists())

    def test_favorite_campaign(self):
        self.client.login(username='contributor', password='password123')
        response = self.client.post(reverse('campaigns:favorite', args=[self.campaign.slug]))
        self.assertEqual(response.status_code, 302)
        from campaigns.models import FavoriteCampaign
        self.assertTrue(FavoriteCampaign.objects.filter(user=self.contributor_user, campaign=self.campaign).exists())
        
        # Unfavorite
        response2 = self.client.post(reverse('campaigns:favorite', args=[self.campaign.slug]))
        self.assertEqual(response2.status_code, 302)
        self.assertFalse(FavoriteCampaign.objects.filter(user=self.contributor_user, campaign=self.campaign).exists())

    def test_creator_profile(self):
        response = self.client.get(reverse('campaigns:creator_profile', args=['creator']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'creator')

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

    def test_add_comment(self):
        self.client.login(username='contributor', password='password123')
        response = self.client.post(reverse('campaigns:comment_add', args=[self.campaign.slug]), {
            'content': 'Great project!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.campaign.comments.filter(content='Great project!').exists())

    def test_reply_comment(self):
        self.client.login(username='contributor', password='password123')
        from .models import CampaignComment
        parent_comment = CampaignComment.objects.create(campaign=self.campaign, user=self.contributor_user, content='First!')
        
        self.client.login(username='creator', password='password123')
        response = self.client.post(reverse('campaigns:comment_reply', args=[parent_comment.id]), {
            'content': 'Thanks!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CampaignComment.objects.filter(parent=parent_comment, content='Thanks!').exists())

    def test_edit_comment(self):
        self.client.login(username='contributor', password='password123')
        from .models import CampaignComment
        comment = CampaignComment.objects.create(campaign=self.campaign, user=self.contributor_user, content='Old')
        
        response = self.client.post(reverse('campaigns:comment_edit', args=[comment.id]), {
            'content': 'New'
        })
        self.assertEqual(response.status_code, 302)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'New')

    def test_edit_comment_unauthorized(self):
        self.client.login(username='creator', password='password123')
        from .models import CampaignComment
        comment = CampaignComment.objects.create(campaign=self.campaign, user=self.contributor_user, content='Old')
        
        response = self.client.post(reverse('campaigns:comment_edit', args=[comment.id]), {
            'content': 'Hacked'
        })
        self.assertEqual(response.status_code, 302)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Old')

    def test_delete_comment(self):
        self.client.login(username='contributor', password='password123')
        from .models import CampaignComment
        comment = CampaignComment.objects.create(campaign=self.campaign, user=self.contributor_user, content='Delete me')
        
        response = self.client.post(reverse('campaigns:comment_delete', args=[comment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CampaignComment.objects.filter(id=comment.id).exists())

    def test_delete_comment_unauthorized(self):
        self.client.login(username='creator', password='password123')
        from .models import CampaignComment
        comment = CampaignComment.objects.create(campaign=self.campaign, user=self.contributor_user, content='Stay')
        
        response = self.client.post(reverse('campaigns:comment_delete', args=[comment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CampaignComment.objects.filter(id=comment.id).exists())

    def test_pin_comment(self):
        from .models import CampaignComment
        comment = CampaignComment.objects.create(campaign=self.campaign, user=self.contributor_user, content='Good question')
        
        self.client.login(username='creator', password='password123')
        response = self.client.post(reverse('campaigns:comment_pin', args=[comment.id]))
        self.assertEqual(response.status_code, 302)
        comment.refresh_from_db()
        self.assertTrue(comment.is_pinned)

    def test_pin_comment_unauthorized(self):
        from .models import CampaignComment
        comment = CampaignComment.objects.create(campaign=self.campaign, user=self.creator_user, content='My comment')
        
        self.client.login(username='contributor', password='password123')
        response = self.client.post(reverse('campaigns:comment_pin', args=[comment.id]))
        self.assertEqual(response.status_code, 302)
        comment.refresh_from_db()
        self.assertFalse(comment.is_pinned)

    def test_report_comment(self):
        from .models import CampaignComment, CommentReport
        comment = CampaignComment.objects.create(campaign=self.campaign, user=self.creator_user, content='Bad stuff')
        
        self.client.login(username='contributor', password='password123')
        response = self.client.post(reverse('campaigns:comment_report', args=[comment.id]), {
            'reason': 'Spam'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CommentReport.objects.filter(comment=comment, user=self.contributor_user, reason='Spam').exists())

    def test_campaign_view_tracking(self):
        # Initial views
        self.assertEqual(self.campaign.views.count(), 0)
        
        # Access campaign detail
        response = self.client.get(reverse('campaigns:detail', args=[self.campaign.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.campaign.views.count(), 1)
        
        # Access again in same session, should not increase
        response = self.client.get(reverse('campaigns:detail', args=[self.campaign.slug]))
        self.assertEqual(self.campaign.views.count(), 1)
        
        # New session
        client2 = Client()
        response2 = client2.get(reverse('campaigns:detail', args=[self.campaign.slug]))
        self.assertEqual(self.campaign.views.count(), 2)

    def test_campaign_analytics_access(self):
        # Unauthorized access
        self.client.login(username='contributor', password='password123')
        response = self.client.get(reverse('campaigns:analytics', args=[self.campaign.slug]))
        self.assertEqual(response.status_code, 302) # Redirects
        
        # Authorized access
        self.client.login(username='creator', password='password123')
        response = self.client.get(reverse('campaigns:analytics', args=[self.campaign.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Campaign Analytics')

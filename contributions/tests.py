from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Profile
from campaigns.models import Category, Campaign, CampaignUpdate
from .models import Contribution
from datetime import date, timedelta

class ContributionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.creator = User.objects.create_user(username='creator', password='password123')
        Profile.objects.create(user=self.creator, user_type='CREATOR')
        
        self.contributor = User.objects.create_user(username='contributor', password='password123')
        Profile.objects.create(user=self.contributor, user_type='CONTRIBUTOR')

        self.category = Category.objects.create(name='Tech')
        
        self.campaign = Campaign.objects.create(
            creator=self.creator,
            title='Test Campaign',
            category=self.category,
            short_description='Short',
            description='Long',
            goal_amount=1000,
            current_amount=0,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            status='ACTIVE'
        )

    def test_support_unauthenticated(self):
        response = self.client.get(reverse('contributions:support', args=[self.campaign.slug]))
        self.assertEqual(response.status_code, 302)

    def test_support_authenticated(self):
        self.client.login(username='contributor', password='password123')
        response = self.client.get(reverse('contributions:support', args=[self.campaign.slug]))
        self.assertEqual(response.status_code, 200)

    def test_invalid_amount(self):
        self.client.login(username='contributor', password='password123')
        response = self.client.post(reverse('contributions:support', args=[self.campaign.slug]), {
            'amount': -50,
            'message': ''
        })
        self.assertEqual(response.status_code, 200) # Form error, returns to page
        self.assertFormError(response, 'form', 'amount', 'Amount must be greater than zero.')

    def test_contribution_flow(self):
        self.client.login(username='contributor', password='password123')
        # Step 1: Submit support form
        response = self.client.post(reverse('contributions:support', args=[self.campaign.slug]), {
            'amount': 500,
            'message': 'Good luck!'
        })
        self.assertEqual(response.status_code, 302)
        contrib = Contribution.objects.first()
        self.assertIsNotNone(contrib)
        self.assertEqual(contrib.amount, 500)
        self.assertEqual(contrib.status, 'PENDING')
        
        # Step 2: Confirm mock payment
        response2 = self.client.post(reverse('contributions:review', args=[contrib.id]))
        self.assertEqual(response2.status_code, 302)
        
        contrib.refresh_from_db()
        self.assertEqual(contrib.status, 'SUCCESS')
        
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.current_amount, 500)
        self.assertEqual(self.campaign.status, 'ACTIVE')
        
        # Step 3: Complete Goal
        response3 = self.client.post(reverse('contributions:support', args=[self.campaign.slug]), {
            'amount': 500,
            'message': 'Finish line!'
        })
        contrib2 = Contribution.objects.exclude(id=contrib.id).first()
        self.client.post(reverse('contributions:review', args=[contrib2.id]))
        
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.current_amount, 1000)
        self.assertEqual(self.campaign.status, 'COMPLETED')

    def test_campaign_update(self):
        self.client.login(username='creator', password='password123')
        response = self.client.post(reverse('campaigns:update_create', args=[self.campaign.slug]), {
            'title': 'New Update',
            'content': 'We made it!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CampaignUpdate.objects.filter(title='New Update').exists())
        
    def test_campaign_update_unauthorized(self):
        self.client.login(username='contributor', password='password123')
        response = self.client.post(reverse('campaigns:update_create', args=[self.campaign.slug]), {
            'title': 'Fake Update',
            'content': 'Ha hacked'
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CampaignUpdate.objects.filter(title='Fake Update').exists())

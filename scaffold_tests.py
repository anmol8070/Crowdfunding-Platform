import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

accounts_tests = """
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.profile_url = reverse('accounts:profile')
        self.edit_profile_url = reverse('accounts:edit_profile')

        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile = Profile.objects.create(user=self.user, user_type='CREATOR')

    def test_registration(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
            'user_type': 'CONTRIBUTOR'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_profile_access_logged_out(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)

    def test_profile_access_logged_in(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.edit_profile_url, {
            'full_name': 'Updated Name',
            'bio': 'New bio',
            'phone': '123456789',
            'location': 'New York'
        })
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.full_name, 'Updated Name')
"""
write_file('accounts/tests.py', accounts_tests)

campaigns_tests = """
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
"""
write_file('campaigns/tests.py', campaigns_tests)

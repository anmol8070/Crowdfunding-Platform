import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

def append_to_file(path, content):
    with open(path, 'a', encoding='utf-8') as f:
        f.write('\n' + content.strip() + '\n')

core_tests = """
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ContactMessage, Notification

class CoreTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='password123')
        
    def test_contact_form(self):
        response = self.client.post(reverse('core:contact'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Help',
            'message': 'Need support'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ContactMessage.objects.filter(email='john@example.com').exists())

    def test_notifications(self):
        self.client.login(username='tester', password='password123')
        notif = Notification.objects.create(
            user=self.user,
            notification_type='INFO',
            title='Test',
            message='Test msg'
        )
        response = self.client.get(reverse('core:notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test msg')
        
        # Mark read
        resp2 = self.client.post(reverse('core:mark_read', args=[notif.id]))
        self.assertEqual(resp2.status_code, 302)
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)
"""
write_file('core/tests.py', core_tests)

campaigns_tests_append = """
    def test_favorite_campaign(self):
        self.client.login(username='contributor', password='password123')
        response = self.client.post(reverse('campaigns:favorite', args=[self.campaign.slug]))
        self.assertEqual(response.status_code, 302)
        from campaigns.models import FavoriteCampaign
        self.assertTrue(FavoriteCampaign.objects.filter(user=self.contributor, campaign=self.campaign).exists())
        
        # Unfavorite
        response2 = self.client.post(reverse('campaigns:favorite', args=[self.campaign.slug]))
        self.assertEqual(response2.status_code, 302)
        self.assertFalse(FavoriteCampaign.objects.filter(user=self.contributor, campaign=self.campaign).exists())

    def test_creator_profile(self):
        response = self.client.get(reverse('campaigns:creator_profile', args=['creator']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'creator')
"""
append_to_file('campaigns/tests.py', campaigns_tests_append)

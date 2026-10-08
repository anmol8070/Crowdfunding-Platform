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

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Event, Registration
from django.utils import timezone
from datetime import timedelta


class EventHubTests(TestCase):
    def setUp(self):
        """Initialize a virtual database environment with test data"""
        self.client = Client()
        # Create a mock student user
        self.user = User.objects.create_user(username='test_stu', password='password123')

        # Create two events with overlapping schedules to test conflict detection.
        now = timezone.now()
        self.event1 = Event.objects.create(
            title="Event 1",
            description="Learn Python",
            location="Boyd Orr Building",
            start_time=now + timedelta(days=1, hours=10),
            end_time=now + timedelta(days=1, hours=12),
        )

        self.event2 = Event.objects.create(
            title="Event 2",
            description="Learn Django",
            location="Sir Williams Building",
            start_time=now + timedelta(days=1, hours=11),
            end_time=now + timedelta(days=1, hours=13),
        )

    def test_1_event_creation(self):
        """Verify that the model saves and retrieves data correctly"""
        self.assertEqual(self.event1.title, "Event 1")
        # Assert that exactly 2 event records exist in the test database
        self.assertEqual(Event.objects.count(), 2)

    def test_2_auth_required_for_registration(self):
        """Ensure unauthenticated users are redirected to login"""
        # Attempt to access the registration page without logging in
        response = self.client.get(reverse('event_register', args=[self.event1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))

    def test_3_m5_time_conflict_prevention(self):
        """Validate the M5 Core Time Conflict Detection algorithm"""
        # Authenticate the test user
        self.client.login(username='test_stu', password='password123')

        # Register for Event 1 successfully
        Registration.objects.create(student=self.user, event=self.event1)
        # Initial registration should be 1
        self.assertEqual(Registration.objects.count(), 1)

        # Attempt to register for Event 2
        response = self.client.post(reverse('event_register', args=[self.event2.id]), {
            'phone': '07700000000',
            'remarks': 'Trying to crash the system'
        })

        # The system must block the registration
        self.assertEqual(Registration.objects.count(), 1)

        # The response must contain the specific error message
        self.assertContains(response, "Time Conflict")

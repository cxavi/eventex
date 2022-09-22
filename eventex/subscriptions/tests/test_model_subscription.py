from django.test import TestCase
from eventex.subscriptions.models import Subscription
from datetime import datetime

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name = 'Carlos Xavier',
            cpf ='12345678901',
            email='96cxavier@gmail.com',
            phone='47992743532'
        )

        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_create_at(self):
        """Subscription must have an auto created attr."""
        self.assertIsInstance(self.obj.created_at, datetime)
    
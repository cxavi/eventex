from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(
            name='Carlos Xavier',
            cpf='12345678901',
            email='96cxavier@gmail.com',
            phone='47992743532'
        )
        self.resp = self.client.get('/inscricao/{}/'.format(self.obj.pk))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)
        
    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_detail.html')

    def test_context(self):
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        contents = ('Carlos Xavier','12345678901',
                  '96cxavier@gmail.com','47992743532')
        with self.subTest():
            for expected in contents:
                self.assertContains(self.resp, expected)

class SubscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get('/inscricao/0/')
        self.assertEqual(404, resp.status_code)
    
from tkinter import E
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from django.core import mail
from eventex.subscriptions.models import Subscription


class SubscribeGet(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """Get /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """HTML must contain input tags"""
        tags = (('<form', 1),
            ('<input', 6),
            ('type="text"', 3),
            ('type="email"',1),
            ('type="submit"', 1))
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)   

    def test_csrf(self):
        """HTML must contais csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)
    

class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name = 'Carlos Xavier', cpf='12345678901',
                    email='96cxavier@gmail.com', phone='47992743532')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST should rediret to /inscricao/1/"""
        self.assertRedirects(self.resp, '/inscricao/1/')

    def test_send_subscribe_email(self):
        """"""
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())
        

class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POSTS should not redirect"""
         
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)
    
    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())



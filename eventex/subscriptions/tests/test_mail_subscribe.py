from django.test import TestCase
from django.core import mail

class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name = 'Carlos Xavier', cpf='12345678901',
                    email='96cxavier@gmail.com', phone='47992743532')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de Inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', '96cxavier@gmail.com']

        self.assertEqual(expect, self.email.to)
    
    def test_subscription_email_body(self):
        contents = [
            'Carlos Xavier',
            '12345678901',
            '96cxavier@gmail.com',
            '47992743532'
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

        
#-*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail

from contact.forms import ContactForm


class ContactTests(TestCase):
    """
    Contact form test.
    """

    def setUp(self):
        """
        Set valid form data.
        """
        self.valid_data={'subject': 'Test subject',
                         'sender_name': 'Steve Tester',
                         'sender_email': 'test@example.com',
                         'message': 'This is my test message',
                         'cc_myself': 'True'}

    def test_contact_form(self):
        """
        Check if contact form validation is working properly.
        """
        invalid_data_dicts = [
            # Empty subject
            {'data': {'subject': '',
                      'sender_name': 'Steve Tester',
                      'sender_email': 'test@example.com',
                      'message': 'This is my test message',
                      'cc_myself': 'False'},
             'error': ('subject', ['This field is required.'])},
            # Empty message
            {'data': {'subject': 'Test subject',
                      'sender_name': 'Steve Tester',
                      'sender_email': 'test@example.com',
                      'message': '',
                      'cc_myself': 'False'},
             'error': ('message', ['This field is required.'])},
            ]

        for invalid_dict in invalid_data_dicts:
            form = ContactForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]], invalid_dict['error'][1])

        form = ContactForm(self.valid_data)
        self.failUnless(form.is_valid())

    def test_send_mail(self):
        """
        Send valid form data by POST and check if email was send with correct
        headers and content.
        """
        response = self.client.post(reverse('contact-form'), self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, self.valid_data['subject'])
        self.assertEqual(mail.outbox[0].from_email, self.valid_data['sender_email'])
        self.assertEqual(mail.outbox[0].to[1], self.valid_data['sender_email'])

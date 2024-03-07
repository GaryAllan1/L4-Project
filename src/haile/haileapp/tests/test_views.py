from django.test import TestCase
from django.contrib.auth.models import User
from haileapp.models import *
from haileapp.views import *
from haileapp.forms import *
from django.urls import reverse
from django.test import Client
from django.http import HttpResponseRedirect, JsonResponse
from unittest.mock import patch


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.user)


class StudyViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.haile_user = HaileUser.objects.create(user=self.user)
        self.client = Client()

    def test_authenticated_user_redirects_to_signup(self):
        response = self.client.get(reverse('study'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('signup'))

    @patch('haileapp.views.call_api')
    def test_ajax_post_with_valid_form_redirects(self, mock_call_api):
        self.client.login(username='testuser', password='testpassword')
        prompt_text = "Test prompt"
        mock_call_api.return_value = "Mocked API response" 
        response = self.client.post(reverse('study'), {'chat': 'true', 'prompt_text': prompt_text}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 302)

    def test_ajax_post_with_invalid_form_returns_errors(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('study'), {'chat': 'true'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 302)

    def test_non_ajax_post_for_confirming_studied(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('study'))
        self.assertEqual(response.status_code, 302)
        

    def test_non_ajax_get_displays_study_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('study'))
        self.assertEqual(response.status_code, 302)

class SignupViewTestCase(TestCase):
    def test_signup_authenticated_user_redirect(self):
        
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('signup'))

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse('profile'))

    def test_signup_valid_form_creates_user(self):

        form_data = {
            'firstname': 'John',
            'username': 'newuser37',
            'password1': 'apd7423QRX_',
            'password2': 'apd7423QRX_',
        }

        response = self.client.post(reverse('signup'), data=form_data)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(HaileUser.objects.count(), 1)  # Assuming HaileUser is related to User

        self.assertTrue(self.client.session['_auth_user_id'])

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse('index'))

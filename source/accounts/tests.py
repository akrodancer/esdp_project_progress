from django.test import TestCase


class TestAccountsAppMethods(TestCase):
    def test_search_user_page(self):
        response = self.client.get('/accounts/search/')
        self.assertEqual(response.status_code, 200)

    def test_registration_page(self):
        response = self.client.get('/accounts/registration/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)
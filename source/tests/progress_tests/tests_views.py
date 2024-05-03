from django.test import TestCase


class TestProgressViews(TestCase):

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_us_page(self):
        response = self.client.get('/about_us/')
        self.assertEqual(response.status_code, 200)

    def test_courses_page(self):
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)

    def test_lessons_page(self):
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, 200)

    def test_all_tests_page(self):
        response = self.client.get('/online_tests/all_tests/')
        self.assertEqual(response.status_code, 200)

    def test_search_user_page(self):
        response = self.client.get('/accounts/search/')
        self.assertEqual(response.status_code, 200)

    def test_registration_page(self):
        response = self.client.get('/accounts/registration/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)
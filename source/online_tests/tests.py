from django.test import TestCase

# Create your online_tests here.
class TestOnlinetestsAppMethods(TestCase):
    def test_all_tests_page(self):
        response = self.client.get('/online_tests/all_tests/')
        self.assertEqual(response.status_code, 200)
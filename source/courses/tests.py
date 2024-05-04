from django.test import TestCase

# Create your online_tests here.
class TestCoursesAppMethods(TestCase):
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
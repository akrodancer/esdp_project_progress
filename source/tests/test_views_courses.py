from django.test import TestCase, Client
from django.urls import reverse
from courses.models import Course, Lesson
from pages.models import PageModel
from django.contrib.auth import get_user_model


class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')

    def test_index_page_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/index.html')

    def test_about_us_view(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/about_us.html')

    def test_courses_view(self):
        response = self.client.get(reverse('courses_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/courses_view.html')

    def test_lessons_view(self):
        response = self.client.get(reverse('lessons_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/lesson_view.html')

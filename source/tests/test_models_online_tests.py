import unittest
from django.test import TestCase
from django.utils import timezone
from unittest.mock import Mock
from online_tests.models import OnlineTest


class OnlineTestTest(TestCase):
    def setUp(self):
        self.test = OnlineTest.objects.create(test_name='Test',
                                              difficulty='Hard',
                                              description='Test description',
                                              test_type='free',
                                              test_language='en',
                                              countdown=timezone.timedelta(minutes=60))

        self.course_mock = Mock()
        self.test.course.add(self.course_mock)

    def test_str_representation(self):
        self.assertEqual(str(self.test), 'Test')

    def test_countdown_formatted_ru_for_one_hour(self):
        self.assertEqual(self.test.countdown_formatted_ru, '60 минут')

    def test_countdown_formatted_ru_for_two_hours(self):
        self.test.countdown = timezone.timedelta(minutes=120)
        self.test.save()
        self.assertEqual(self.test.countdown_formatted_ru, '2 часа 0 минут')

    def test_countdown_formatted_kg_for_one_hour(self):
        self.assertEqual(self.test.countdown_formatted_kg, '60 мүнөт')

    def test_countdown_formatted_kg_for_two_hours(self):
        self.test.countdown = timezone.timedelta(minutes=120)
        self.test.save()
        self.assertEqual(self.test.countdown_formatted_kg, '2 саат 0 мүнөт')

    def test_is_accessible_by_for_free_test(self):
        user_mock = Mock()
        self.assertTrue(self.test.is_accessible_by(user_mock))

    def test_is_accessible_by_for_paid_test_not_paid_by_user(self):
        user_mock = Mock()
        self.test.test_type = 'paid'
        self.test.course.first().is_paid_by.return_value = False
        self.test.save()
        self.assertFalse(self.test.is_accessible_by(user_mock))

    def test_is_accessible_by_for_paid_test_paid_by_user(self):
        user_mock = Mock()
        self.test.test_type = 'paid'
        self.test.course.first().is_paid_by.return_value = True
        self.test.save()
        self.assertTrue(self.test.is_accessible_by(user_mock))


if __name__ == '__main__':
    unittest.main()

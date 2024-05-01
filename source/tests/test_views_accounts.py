import unittest
from unittest.mock import Mock, patch
from django.shortcuts import redirect
from accounts import views


class LogoutViewTest(unittest.TestCase):
    def setUp(self):
        self.request = Mock()

    def test_logout_view_redirects_to_courses_index_after_logout(self):
        result = views.logout_view(self.request)
        self.assertEqual(result.url, redirect('courses:index').url)

    @patch('accounts.views.logout')
    def test_logout_view_calls_logout_with_request(self, logout_mocked):
        views.logout_view(self.request)
        logout_mocked.assert_called_once_with(self.request)

    @patch('accounts.views.redirect')
    def test_logout_view_redirects_to_courses_index(self, redirect_mocked):
        views.logout_view(self.request)
        redirect_mocked.assert_called_once_with('courses:index')


if __name__ == '__main__':
    unittest.main()

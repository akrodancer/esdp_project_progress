import unittest
from unittest.mock import patch
from django.contrib import admin
from online_tests.admin import AnswerInline
from online_tests.models import Answer


@patch("online_tests.admin.admin")
class TestAnswerInline(unittest.TestCase):

    def setUp(self):
        self.inline = AnswerInline(parent_model=admin.site, admin_site=admin.site)

    def test_model(self):
        self.assertEqual(self.inline.model, Answer)

    def test_extra(self):
        self.assertEqual(self.inline.extra, 0)

    def test_fields(self):
        expected_fields = ('answer_text', 'answer_image', 'is_correct')
        self.assertEqual(self.inline.fields, expected_fields)

    def test_fk_name(self):
        self.assertEqual(self.inline.fk_name, 'question')


if __name__ == '__main__':
    unittest.main()

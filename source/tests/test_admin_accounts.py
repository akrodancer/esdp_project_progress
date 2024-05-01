import unittest
from unittest.mock import MagicMock


class admin:
    class StackedInline:
        pass


class Comment:
    pass


from accounts.admin import CommentsInline


class TestCommentsInline(unittest.TestCase):
    def test_model(self):
        self.assertEqual(CommentsInline.model, Comment)

    def test_extra(self):
        self.assertEqual(CommentsInline.extra, 0)

    def test_readonly_fields(self):
        self.assertEqual(
            CommentsInline.readonly_fields, ('teacher', 'content', 'created_at'))

    def test_fk_name(self):
        self.assertEqual(CommentsInline.fk_name, 'student')


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import MagicMock
from courses.admin import VisitInline


class VisitInlineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.visit_inline = VisitInline(model=MagicMock(), admin_site=MagicMock())

    def test_fields(self):
        self.assertEqual(self.visit_inline.fields, ('students', 'is_currently_viewing', 'grade'))

    def test_extra(self):
        self.assertEqual(self.visit_inline.extra, 0)


if __name__ == '__main__':
    unittest.main()

# Import the required modules
import unittest
from unittest import mock
from pages import admin  # Assuming admin is a module in 'pages'


class TestCarouselMainInline(unittest.TestCase):

    @mock.patch.object(admin.CarouselMainInline, 'model')
    @mock.patch.object(admin.CarouselMainInline, 'extra')
    @mock.patch.object(admin.CarouselMainInline, 'fields')
    def setUp(self, mock_model, mock_extra, mock_fields):
        self.testCarousel = admin.CarouselMainInline(mock_model, mock_extra, mock_fields)

    def test_model(self):
        self.assertEqual(self.testCarousel.model, 'CarouselMainModel', 'Model is incorrect')

    def test_extra(self):
        self.assertEqual(self.testCarousel.extra, 0, 'Extra values are incorrect')

    def test_fields(self):
        fields = [field.name for field in self.mock_model._meta.get_fields()]
        self.assertEqual(self.testCarousel.fields, fields, 'Fields are incorrect')


if __name__ == '__main__':
    unittest.main()

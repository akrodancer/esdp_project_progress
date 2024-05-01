import unittest
from unittest.mock import MagicMock
from pages import context_processor


class PageTextDisplayTest(unittest.TestCase):

    def setUp(self):
        self.mock_request = MagicMock()

    def test_page_text_display_get_request(self):
        self.mock_request.method = 'GET'
        self.mock_request.path = '/test'
        context_processor.PageModel.objects.get = MagicMock(return_value='test_page')

        expected_result = {
            'page': 'test_page'
        }
        result = context_processor.page_text_display(self.mock_request)
        self.assertEqual(result, expected_result)

    def test_page_text_display_get_request_no_page(self):
        self.mock_request.method = 'GET'
        self.mock_request.path = 'not_exsting_page_test'
        context_processor.PageModel.objects.get = MagicMock(side_effect=Exception)

        expected_result = {}
        result = context_processor.page_text_display(self.mock_request)
        self.assertEqual(result, expected_result)

    def test_page_text_display_non_get_request(self):
        self.mock_request.method = 'POST'

        expected_result = {}
        result = context_processor.page_text_display(self.mock_request)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()

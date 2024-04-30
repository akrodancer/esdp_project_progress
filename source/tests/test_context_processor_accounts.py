import unittest
from unittest import mock
from accounts import context_processor


class TestLogInProcessor(unittest.TestCase):

    @mock.patch('accounts.context_processor.LoginUserForm')
    def test_login_processor_get_request(self, mock_form):
        mock_form.return_value = 'form_data'
        mock_request = mock.Mock()

        mock_request.method = 'GET'
        expected_output = {
            'form_log': 'form_data',
        }

        actual_output = context_processor.log_in_processor(mock_request)

        self.assertEqual(expected_output, actual_output, "Failed: GET request result doesn't match expected output")

    @mock.patch('accounts.context_processor.LoginUserForm')
    def test_login_processor_get_request_exception_handle(self, mock_form):
        mock_form.side_effect = Exception
        mock_request = mock.Mock()

        mock_request.method = 'GET'
        expected_output = {}

        actual_output = context_processor.log_in_processor(mock_request)

        self.assertEqual(expected_output, actual_output, "Failed: GET request with exception doesn't handle properly")

    def test_login_processor_non_get_request(self):
        mock_request = mock.Mock()

        mock_request.method = 'POST'
        expected_output = {}

        actual_output = context_processor.log_in_processor(mock_request)

        self.assertEqual(expected_output, actual_output, "Failed: Non-GET request doesn't return empty dictionary")


if __name__ == "__main__":
    unittest.main()

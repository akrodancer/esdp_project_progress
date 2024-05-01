import json
import unittest
from unittest.mock import Mock
from accounts.json_form_handler import JsonFormHandler


class TestJsonFormHandler(unittest.TestCase):
    def setUp(self):
        self.mock_form = Mock()
        self.mock_request = Mock()

    def test_create_object_valid_json(self):
        self.mock_request.body.decode.return_value = "{\"key\": \"value\"}"
        self.mock_form.is_valid.return_value = True
        json_formhandler = JsonFormHandler(self.mock_request, self.mock_form)

        json_formhandler.create_object()
        result = json_formhandler.response()

        self.assertEqual(result, {'result': 'ok'})

    def test_create_object_invalid_json(self):
        self.mock_request.body.decode.return_value = "{\"key\": \"value\"}"
        self.mock_form.is_valid.return_value = False
        json_formhandler = JsonFormHandler(self.mock_request, self.mock_form)

        json_formhandler.create_object()
        result = json_formhandler.response()

        self.assertEqual(result, {'result': 'wrong_data'})

    def test_create_object_exception(self):
        self.mock_request.body.decode.side_effect = Exception()
        json_formhandler = JsonFormHandler(self.mock_request, self.mock_form)

        json_formhandler.create_object()
        result = json_formhandler.response()

        self.assertEqual(result, {'result': 'error'})


if __name__ == '__main__':
    unittest.main()

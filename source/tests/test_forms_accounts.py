import unittest
from unittest import mock
from accounts import forms


class TestMeta(unittest.TestCase):

    @mock.patch('accounts.forms.Comment', spec=True)
    def setUp(self, mock_comment_model):
        class Meta:
            model = mock_comment_model
            fields = ['content']
            widgets = {
                'content': forms.Textarea(),
            }
            labels = {
                'content': '',
            }

        self.meta = Meta()

    def test_model_type(self):
        self.assertIsInstance(self.meta.model, type, "Model is not of 'type' type")

    def test_fields_type(self):
        self.assertIsInstance(self.meta.fields, list, "Fields is not a list")

    def test_widgets_type(self):
        self.assertIsInstance(self.meta.widgets, dict, "Widgets is not a dict")

    def test_labels_type(self):
        self.assertIsInstance(self.meta.labels, dict, "Labels is not a dict")


if __name__ == '__main__':
    unittest.main()

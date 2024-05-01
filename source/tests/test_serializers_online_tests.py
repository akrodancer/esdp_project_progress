import unittest
from online_tests.serializers import AnswerSerializer
from rest_framework import serializers
from django.core.files import File


class TestAnswerSerializer(unittest.TestCase):
    def setUp(self):
        self.serializer_data = {'id': 1, 'is_correct': True, 'answer_text': 'Answer text',
                                'answer_image': File(open('path_to_image.jpg'))}

    def test_contains_expected_fields(self):
        serializer = AnswerSerializer()
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'is_correct', 'answer_text', 'answer_image']))

    def test_is_correct_field_content(self):
        serializer = AnswerSerializer(data=self.serializer_data)
        self.assertEqual(serializer.data.get('is_correct'), self.serializer_data.get('is_correct'))

    def test_answer_text_field_content(self):
        serializer = AnswerSerializer(data=self.serializer_data)
        self.assertEqual(serializer.data.get('answer_text'), self.serializer_data.get('answer_text'))

    def test_answer_image_field_content(self):
        serializer = AnswerSerializer(data=self.serializer_data)
        self.assertEqual(serializer.data.get('answer_image'), self.serializer_data.get('answer_image'))


if __name__ == '__main__':
    unittest.main()

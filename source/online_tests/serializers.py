from rest_framework import serializers

from .models import Question, Answer, UserTest, OnlineTest


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'is_correct', 'answer_text', 'answer_image']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_name', 'question_text', 'question_image', 'answers']


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = OnlineTest
        fields = ['id', 'test_name', 'difficulty', 'test_type', 'questions', 'countdown']


class UserTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTest
        fields = ['user', 'correct_answer_count', 'incorrect_answer_cnt', 'test', 'attempts']

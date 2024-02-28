from rest_framework import serializers

from .models import Test, Question, Answer, UserTest, UserAnswer


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'test_name', 'difficulty', 'test_type', 'course']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_name', 'question_text', 'question_image', 'test']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'is_correct', 'answer_text', 'answer_image', 'question']


class UserTestSerializer(serializers.ModelSerializer):
    correct_answers = serializers.SerializerMethodField()
    incorrect_answers = serializers.SerializerMethodField()

    class Meta:
        model = UserTest
        fields = ['id', 'user', 'test', 'date_taken', 'correct_answers', 'incorrect_answers']

    def get_correct_answers(self, obj):
        correct, _ = obj.count_answers()
        return correct

    def get_incorrect_answers(self, obj):
        _, incorrect = obj.count_answers()
        return incorrect


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['id', 'user_test', 'question', 'answer']

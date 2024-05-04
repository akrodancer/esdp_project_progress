from django.test import TestCase
from unittest.mock import Mock, patch
from online_tests.views import AllTestsView

# Create your online_tests here.
class TestOnlinetestsAppMethods(TestCase):
    def setUp(self):
        # Настраиваем объект view и подменяем запро
        self.view = AllTestsView()
        self.view.request = Mock()

    @patch('online_tests.views.OnlineTest.objects')
    def test_get_context_data_ru(self, mock_objects):
        # Настраиваем мок-объекты
        mock_objects.all.return_value.filter.return_value = ['тест1', 'тест2']
        self.view.request.GET.get.return_value = 'RU'

        # Вызываем тестируемую функцию
        context = self.view.get_context_data()

        # Проверяем результат
        self.assertEqual(context['tests'], ['тест1', 'тест2'])
        mock_objects.all.assert_called_once()
        mock_objects.all.return_value.filter.assert_called_once_with(test_language='русский')

    @patch('online_tests.views.OnlineTest.objects')
    def test_get_context_data_kg(self, mock_objects):
        # Настраиваем мок-объекты
        mock_objects.all.return_value.filter.return_value = ['тест3', 'тест4']
        self.view.request.GET.get.return_value = 'KG'

        # Вызываем тестируемую функцию
        context = self.view.get_context_data()

        # Проверяем результат
        self.assertEqual(context['tests'], ['тест3', 'тест4'])
        mock_objects.all.assert_called_once()
        mock_objects.all.return_value.filter.assert_called_once_with(test_language='кыргызский')

    @patch('online_tests.views.OnlineTest.objects')
    def test_get_context_data_else(self, mock_objects):
        # Настраиваем мок-объекты
        mock_objects.all.return_value = ['тест5', 'тест6']
        self.view.request.GET.get.return_value = 'EN'

        # Вызываем тестируемую функцию
        context = self.view.get_context_data()

        # Проверяем результат
        self.assertEqual(context['tests'], ['тест5', 'тест6'])
        mock_objects.all.assert_called_once()
    def test_all_tests_page(self):
        response = self.client.get('/online_tests/all_tests/')
        self.assertEqual(response.status_code, 200)
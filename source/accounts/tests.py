from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from datetime import date
from django.http import Http404
from .models import User, Comment
from courses.models import Visit, Course
from .views import StudentDetailView
from unittest.mock import Mock
from accounts.json_form_handler import JsonFormHandler
import unittest

class UserRegisterViewTestCase(TestCase):
    def setUp(self):
        self.register_url = reverse('accounts:user_reg')

    def test_register(self):
        response = self.client.post(self.register_url, {
            'username': 'user',
            'password1': 'password',
            'password2': 'password',
            'email': 'example@email.com',
            'phone': '+996 (111)-111-111'
        })
        self.assertRedirects(response, reverse('courses:index'))
        user = User.objects.filter(username='user').first()
        self.assertIsNotNone(user)
        self.assertTrue(self.client.session['_auth_user_id'])


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.login_url = reverse('accounts:log_in')

    def test_login_valid_user(self):
        user = User.objects.create_user(username='user', password='password')
        response = self.client.post(self.login_url, {'username': 'user', 'password': 'password'})
        self.assertRedirects(response, reverse('courses:index'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_invalid_user(self):
        response = self.client.post(self.login_url, {'username': 'username', 'password': 'password111'})
        self.assertRedirects(response, reverse('courses:index'))
        self.assertFalse('_auth_user_id' in self.client.session)


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.logout_url = reverse('accounts:log_out')

    def test_logout(self):
        user = User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, reverse('courses:index'))
        self.assertFalse('_auth_user_id' in self.client.session)


class StudentDetailViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='user', role='user', email='student1@example.com')
        self.teacher = User.objects.create_user(username='teacher', role='teacher', email='teacher1@example.com')
        self.course = Course.objects.create(course_name='Course', date_start=date.today(),
                                            date_finish=date.today())
        self.course.teacher.add(self.teacher)
        self.course.students.add(self.user)

    def test_get_success(self):
        course_id = self.course.id
        request = self.factory.get(f'/student/1/?course={course_id}')
        request.user = self.user
        response = StudentDetailView.as_view()(request, pk=self.user.pk)
        self.assertEqual(response.status_code, 200)
        self.assertIn('student', response.context_data)
        self.assertIn('teachers', response.context_data)
        self.assertIn('selected_course', response.context_data)

    def test_get_invalid_role(self):
        request = self.factory.get('/student/2/?course=1')
        request.user = self.teacher
        with self.assertRaises(Http404):
            StudentDetailView.as_view()(request, pk=self.teacher.pk)

    def test_get_missing_course(self):
        request = self.factory.get('/student/1/')
        request.user = self.user
        with self.assertRaises(Http404):
            StudentDetailView.as_view()(request, pk=self.user.pk)


class CommentCreateViewTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher', password='password',
                                                role='teacher', email='teacher1@example.com')
        self.student = User.objects.create_user(username='student', password='password',
                                                role='student', email='student1@example.com')
        self.course = Course.objects.create(course_name='Course', date_start=date.today(),
                                            date_finish=date.today())
        self.course.teacher.add(self.teacher)
        self.course.students.add(self.student)
        self.client = Client()
        self.client.login(username='teacher', password='password')

    def test_can_create_comment(self):
        url = reverse('accounts:add_comment', kwargs={'pk': self.student.pk})
        url += f'?course={self.course.id}'
        data = {'content': 'Test comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'Test comment')
        self.assertEqual(comment.teacher, self.teacher)
        self.assertEqual(comment.student, self.student)

    def test_cant_create_comment(self):
        self.client.logout()
        self.client.login(username='student', password='password')
        url = reverse('accounts:add_comment', kwargs={'pk': self.student.pk})
        url += f'?course={self.course.id}'
        data = {'content': 'Test comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Comment.objects.count(), 0)


class StudentListViewTest(TestCase):
    def setUp(self):
        self.student1 = User.objects.create_user(username='student1', password='password', role='user',
                                                 first_name='Иван', last_name='Иванов', email='student1@example.com')
        self.course = Course.objects.create(course_name="Test Course", date_start=date.today(),
                                            date_finish=date.today())
        self.student1.enrolled_courses.add(self.course)
        self.client = Client()

    def test_student_list_empty(self):
        response = self.client.get(reverse('accounts:search_student'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['students'], [])

    def test_student_list_fullname(self):
        response = self.client.get(reverse('accounts:search_student') + '?student=Иван+Иванов')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['students'], [self.student1])

    def test_student_list_name(self):
        response = self.client.get(reverse('accounts:search_student') + '?student=Иван')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['students'], [])

    def test_student_list_not_exist(self):
        response = self.client.get(reverse('accounts:search_student') + '?student=Андрей+Андреев')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['students'], [])

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


class CommentDeleteViewTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher', password='password', role='teacher', email='teacher1@example.com'
        )
        self.student = User.objects.create_user(
            username='student', password='password', role='student', email='student1@example.com'
        )
        self.course = Course.objects.create(course_name='Course', date_start=date.today(),
                                            date_finish=date.today())
        self.course.teacher.add(self.teacher)
        self.course.students.add(self.student)
        self.comment = Comment.objects.create(
            content='Test comment', teacher=self.teacher, student=self.student, course_id=self.course.id
        )
        self.client = Client()

    def test_teacher_can_delete_comment(self):
        self.client.login(username='teacher', password='password')
        response = self.client.post(
            reverse('accounts:delete_comment', kwargs={'pk': self.comment.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_student_cannot_delete_comment(self):
        self.client.login(username='student', password='password')
        response = self.client.post(
            reverse('accounts:delete_comment', kwargs={'pk': self.comment.pk})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_unauthenticated_user_cannot_delete_comment(self):
        response = self.client.post(
            reverse('accounts:delete_comment', kwargs={'pk': self.comment.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())


class CommentUpdateViewTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher', password='password', role='teacher', email='teacher1@example.com'
        )
        self.student = User.objects.create_user(
            username='student', password='password', role='student', email='student1@example.com'
        )
        self.course = Course.objects.create(course_name='Course', date_start=date.today(),
                                            date_finish=date.today())
        self.course.teacher.add(self.teacher)
        self.course.students.add(self.student)
        self.comment = Comment.objects.create(
            content='Test comment', teacher=self.teacher, student=self.student, course_id=self.course.id
        )
        self.client = Client()

    def test_teacher_can_update_comment(self):
        self.client.login(username='teacher', password='password')
        new_content = 'Updated comment'
        response = self.client.post(
            reverse('accounts:update_comment', kwargs={'pk': self.comment.pk}),
            {'content': new_content},
        )
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, new_content)

    def test_student_cannot_update_comment(self):
        self.client.login(username='student', password='password')
        new_content = 'Updated comment'
        response = self.client.post(
            reverse('accounts:update_comment', kwargs={'pk': self.comment.pk}),
            {'content': new_content},
        )
        self.assertEqual(response.status_code, 403)
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.content, new_content)

    def test_unauthenticated_user_cannot_update_comment(self):
        new_content = 'Updated comment'
        response = self.client.post(
            reverse('accounts:update_comment', kwargs={'pk': self.comment.pk}),
            {'content': new_content},
        )
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.content, new_content)

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from lms.models import Course, Lesson, Subscription


class CourseLessonSubscriptionTests(APITestCase):

    def setUp(self):
        self.lesson_url = reverse('lms:lesson-list')
        self.subscribe_url = reverse('lms:subscribe')
        self.course_url = reverse('lms:course-list')
        self.User = get_user_model()
        self.regular_user = self.User.objects.create_user(
            email='testuser@example.com',
            password='password',
            first_name='TestUser',
        )

        self.moderator_user = self.User.objects.create_user(
            email='moderator@example.com',
            password='moderator_password',
            first_name='Moderator',
        )

        moderator_permission = Permission.objects.get(codename='moderator')
        self.moderator_user.user_permissions.add(moderator_permission)

        self.course1 = Course.objects.create(title='Course 1', description='Description 1', autor=self.regular_user)
        self.course2 = Course.objects.create(title='Course 2', description='Description 2', autor=self.regular_user)

        self.lesson1 = Lesson.objects.create(
            title='Lesson 1',
            description='Description 1',
            video_link='https://youtube.com/watch?v=example',
            course=self.course1,
            autor=self.regular_user
        )

    def test_create_lesson(self):
        """
        Тест создания урока пользователем
        """
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'title': 'Lesson 2',
            'description': 'Lesson description',
            'video_link': 'https://youtube.com/watch?v=example',
            'course': self.course1.id,
            'autor': self.regular_user.id
        }

        response = self.client.post(self.lesson_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_forbidden_for_moderator(self):
        """
        Тест запрета на создание урока для модератора
        """
        self.client.force_authenticate(user=self.moderator_user)
        data = {
            'title': 'Lesson 3',
            'description': 'Lesson description',
            'course': self.course1.id
        }
        response = self.client.post(self.lesson_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscription_add(self):
        """
        Тест добавления подписки
        """
        self.client.force_authenticate(user=self.regular_user)
        data = {'id': self.course1.id}

        response = self.client.post(self.subscribe_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')

        self.assertTrue(Subscription.objects.filter(user=self.regular_user, course=self.course1).exists())

    def test_subscription_remove(self):
        """
        Тест удаления подписки
        """
        Subscription.objects.create(user=self.regular_user, course=self.course1)
        self.client.force_authenticate(user=self.regular_user)
        data = {'id': self.course1.id}

        response = self.client.delete(self.subscribe_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')

        self.assertFalse(Subscription.objects.filter(user=self.regular_user, course=self.course1).exists())

    def test_subscription_list(self):
        """
        Тест получения списка подписок
        """
        Subscription.objects.create(user=self.regular_user, course=self.course1)
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.get(self.subscribe_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Course 1', response.data['subscribed_courses'])

    def test_moderator_can_view_all_courses(self):
        """
        Тест, что модератор может просматривать все курсы
        """
        self.client.force_authenticate(user=self.moderator_user)

        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), Course.objects.count())

    def test_access_single_lesson(self):
        """
        Тест доступа к одному уроку
        """
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('lms:lesson-detail', args=[self.lesson1.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson1.title)

    def test_edit_lesson(self):
        """
        Тест редактирования урока
        """
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('lms:lesson-detail', args=[self.lesson1.id])
        data = {
            'title': 'Updated Lesson 1',
            'description': 'Updated description',
            'video_link': 'https://youtube.com/watch?v=updated_example',
            'course': self.course1.id,
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson1.refresh_from_db()
        self.assertEqual(self.lesson1.title, 'Updated Lesson 1')

    def test_delete_lesson(self):
        """
        Тест удаления урока
        """
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('lms:lesson-detail', args=[self.lesson1.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson1.id).exists())

    def test_create_lesson_invalid_video_link(self):
        """
        Тест создания урока с некорректной ссылкой на видео
        """
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'title': 'Lesson 4',
            'description': 'Lesson description',
            'video_link': 'https://example.com/watch?v=not_youtube',
            'course': self.course1.id,
            'autor': self.regular_user.id
        }

        response = self.client.post(self.lesson_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('Поле video_link должно содержать ссылку только на YouTube.', response.data['non_field_errors'])

    def test_list_user_lessons(self):
        """
        Тест на отображение списка всех уроков юзера
        """
        Lesson.objects.create(
            title='Lesson 5',
            description='Description 5',
            video_link='https://youtube.com/watch?v=another_example',
            course=self.course1,
            autor=self.regular_user
        )
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.get(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

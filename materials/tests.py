from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from materials.models import Course, Lesson, Subscription
from users.models import User

class LessonTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = self.create_user("test4@test4.ru", is_superuser=True, is_staff=True, is_active=True)
        self.course = self.create_course("Test", "Test", self.user)
        self.lesson = self.create_lesson("Test", "Test_lesson", self.user, self.course)

        access_token = self.get_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def create_user(self, email, **kwargs):
        user = User.objects.create(email=email, **kwargs)
        user.set_password("test")
        user.save()
        return user

    def create_course(self, title, description, owner):
        return Course.objects.create(title=title, description=description, owner=owner)

    def create_lesson(self, title, description, owner, course):
        return Lesson.objects.create(title=title, description=description, owner=owner, course=course)

    def get_access_token(self, user):
        return str(RefreshToken.for_user(user).access_token)

    def test_create_lesson(self):
        data = {
            "title": "Test8 Django",
            "description": "Test8",
            "url": "https://www.youtube.com/watch?v=N2acITrfzHQ",
            "course": str(self.course.id)
        }

        response = self.client.post(reverse('materials:lesson_create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], data['title'])

    def test_create_lesson_validation_error(self):
        data = {
            "title": "Test9 Django",
            "description": "Test9",
            "url": "https://rutube.ru/video/8dfjt5j4j7dfi3/",
            "course": str(self.course.id)
        }

        response = self.client.post(reverse('materials:lesson_create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Нельзя использовать ссылки на сторонние сайты']})

    def test_list_lesson(self):
        response = self.client.get(reverse('materials:lesson_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], self.lesson.title)

    def test_retrieve_lesson(self):
        response = self.client.get(reverse('materials:lesson_get', args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_update_lesson(self):
        updated_data = {
            "description": "Updated lesson",
            "url": "https://www.youtube.com/watch?v=N2acITrfzHQ"
        }

        response = self.client.patch(reverse('materials:lesson_update', args=[self.lesson.id]), updated_data)
        self.lesson.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], updated_data['description'])

    def test_delete_lesson(self):
        response = self.client.delete(reverse('materials:lesson_delete', args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = self.create_user("test4@test4.ru", is_superuser=True, is_staff=True, is_active=True)
        self.course = self.create_course("Test", "Test", self.user)
        self.subscribe = self.create_subscription(self.user, self.course)

        access_token = self.get_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def create_user(self, email, **kwargs):
        user = User.objects.create(email=email, **kwargs)
        user.set_password("test")
        user.save()
        return user

    def create_course(self, title, description, owner):
        return Course.objects.create(title=title, description=description, owner=owner)

    def create_subscription(self, user, course):
        return Subscription.objects.create(user=user, course=course)

    def get_access_token(self, user):
        return str(RefreshToken.for_user(user).access_token)

    def test_subscribe_to_course(self):
        data = {
            "user": self.user.id,
            "course": self.course.id
        }

        response = self.client.post(reverse('materials:subscription'), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')

    def test_unsubscribe_to_course(self):
        data = {
            "user": self.user.id,
            "course": self.course.id
        }

        response = self.client.post(reverse('materials:subscription'), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')


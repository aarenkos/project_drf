from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=12, **NULLABLE, verbose_name='телефон')
    city = models.CharField(max_length=100, **NULLABLE, verbose_name='город')
    avatar = models.ImageField(upload_to="avatars", **NULLABLE, verbose_name='аватарка')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = (
        ('CASH', 'наличные'),
        ('TRANSFER', 'перевод'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateField(auto_now=True, verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='оплаченный курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name='оплаченный урок')
    payment_amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='сумма платежа')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, verbose_name='способ оплаты')

    def __str__(self):
        return f"{self.user} - {self.payment_amount} - {self.payment_date}"

    class Meta:
        verbose_name = "платёж"
        verbose_name_plural = "платежи"

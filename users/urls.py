from django.urls import path
# from rest_framework.routers import DefaultRouter

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('payment/', views.PaymentsListAPIView.as_view(), name='payments_list'),
]

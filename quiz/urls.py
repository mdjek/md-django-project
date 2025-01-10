from django.urls import path
from . import views

urlpatterns = [
    path('', views.enter_test, name='home'),  # Корневой путь
    path('signup/', views.signup, name='signup'),
    path('enter-test/', views.enter_test, name='enter_test'),
    path('take-test/<int:test_id>/', views.take_test, name='take_test'),
]
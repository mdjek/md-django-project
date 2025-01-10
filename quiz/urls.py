from django.urls import path
from . import views
from .views import TestView, AccessTestView

urlpatterns = [
    path('', AccessTestView.as_view(), name='home'),  # Корневой путь
    path('sign-up', views.sign_up, name='sign_up'),
    path('access-test', AccessTestView.as_view(), name='access_test'),
    path('tests/<int:test_id>', TestView.as_view(), name='take_test'),
]
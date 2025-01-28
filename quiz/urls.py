from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import TestView, AccessTestView, SignUpView, UserTestResultsView, TestDescriptionView

urlpatterns = [
    path("", AccessTestView.as_view(), name="home"),
    path("sign-up", SignUpView.as_view(), name="sign_up"),
    path("log-in", LoginView.as_view(), name="log_in"),
    path("log-out", LogoutView.as_view(), name="log_out"),
    path("access-test", AccessTestView.as_view(), name="access_test"),
    path("test/<int:test_id>/description", TestDescriptionView.as_view(), name="test_description"),
    path("test/<int:test_id>/", TestView.as_view(), name="take_test"),
    path("results", UserTestResultsView.as_view(), name="user_results"),
]

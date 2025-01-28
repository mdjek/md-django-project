from django.contrib import admin
from django.urls import path, include

# custom error handlers
handler404 = "quiz.views.custom_page_not_found_view"
handler500 = "quiz.views.custom_error_view"
handler403 = "quiz.views.custom_permission_denied_view"
handler400 = "quiz.views.custom_bad_request_view"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("quiz.urls")),
]

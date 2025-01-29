from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import TestView, AccessTestView, SignUpView, UserTestResultsView, TestDescriptionView, \
    TestCreateView, TestUpdateView, TestDeleteView, TestListView, TestStatisticsView, QuestionListView, \
    QuestionCreateView, QuestionUpdateView, QuestionDeleteView, AnswerAddView, AnswerUpdateView, AnswerDeleteView, \
    QuestionGetView, AnswerGetView, MainPageView

urlpatterns = [
    # Главная страница
    path('', MainPageView.as_view(), name='home'),
    
    # Страница регистрации
    path('sign-up', SignUpView.as_view(), name='sign_up'),
    
    # Страница входа
    path('log-in', LoginView.as_view(template_name='registration/login.html'), name='log_in'), 
    
    # Страница выхода
    path('log-out', LogoutView.as_view(), name='log_out'),  # Добавляем маршрут для выхода
    
    # Страница доступа к тесту (возможно, дублируется с 'home')
    path('access-test', AccessTestView.as_view(), name='access_test'),
    
    # Описание теста по его ID
    path('test/<int:test_id>/description', TestDescriptionView.as_view(), name='test_description'),
    
    # Пройти тест по его ID
    path('test/<int:test_id>/', TestView.as_view(), name='take_test'),
    
    # Результаты пользователя
    path('results', UserTestResultsView.as_view(), name='user_results'),
    
    # URL маршруты для управления тестами
    # Создание нового теста
    path('test/create/', TestCreateView.as_view(), name='test_create'),
    
    # Обновление существующего теста по его ID
    path('test/<int:pk>/update/', TestUpdateView.as_view(), name='test_update'),
    
    # Удаление существующего теста по его ID
    path('test/<int:pk>/delete/', TestDeleteView.as_view(), name='test_delete'),
    
    # Список всех тестов (для администраторов)
    path('tests/', TestListView.as_view(), name='test_list'),
    
    # Статистика по конкретному тесту
    path('test/<int:test_id>/statistics/', TestStatisticsView.as_view(), name='test_statistics'),

    # Список вопросов к конкретному тесту
    path('test/<int:test_id>/questions/', QuestionListView.as_view(), name='question_list'),

    path('test/<int:test_id>/question/create/', QuestionCreateView.as_view(), name='question_create'),

    path('test/<int:test_id>/question/<int:question_id>/update/', QuestionUpdateView.as_view(), name='question_update'),

    path('test/<int:test_id>/question/<int:question_id>/delete/', QuestionDeleteView.as_view(), name='question_delete'),

    path('test/<int:test_id>/question/<int:question_id>/answer/add/', AnswerAddView.as_view(), name='answer_add'),

    path('test/<int:test_id>/question/<int:question_id>/answer/<int:answer_id>/update/', AnswerUpdateView.as_view(), name='answer_update'),

    path('test/<int:test_id>/question/<int:question_id>/answer/<int:answer_id>/delete/', AnswerDeleteView.as_view(), name='answer_delete'),

    path('test/<int:test_id>/question/<int:question_id>/', QuestionGetView.as_view(), name='get_question'),

    path('test/<int:test_id>/question/<int:question_id>/answer/<int:answer_id>/', AnswerGetView.as_view(), name='get_answer'),
]
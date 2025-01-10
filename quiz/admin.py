from django.contrib import admin
from quiz.models import Subject, Test, Question, Answer, UserTestResult

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'start_time', 'end_time', 'duration', 'access_key')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'score')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')

@admin.register(UserTestResult)
class UserTestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'completed_at')
from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Test(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    pass_score = models.IntegerField(default=100)  # Проходной балл
    start_time = models.DateTimeField()  # Начало теста
    end_time = models.DateTimeField()  # Окончание теста
    duration = models.IntegerField()  # Длительность теста в минутах
    access_key = models.CharField(max_length=50, unique=True)  # Ключ доступа
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests', null=True, blank=True)  # Разрешаем NULL значения

    def __str__(self):
        return self.name

class Question(models.Model):
    TYPE_CHOICES = [
        (1, 'Single Choice'),
        (2, 'Multiple Choice'),
        (3, 'Text Response')
    ]
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField(default=10)  # Балл за вопрос
    type = models.IntegerField(choices=TYPE_CHOICES)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class UserTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.test.name} - {self.score}"
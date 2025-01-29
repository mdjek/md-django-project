# views.py
from django import views
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, mixins
from django.utils import timezone
from quiz.models import Test, Question, UserTestResult, Subject, Answer
from quiz.forms import SignUpForm, TestAccessForm, TestForm, QuestionForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import secrets
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group


def custom_page_not_found_view(request, exception):
    return render(request, "system/error_page.html", {"title": "Страница не найдена", "status": 404})


def custom_error_view(request, exception=None):
    return render(request, "system/error_page.html", {"title": "Внутренняя ошибка сайта", "status": 500})


def custom_permission_denied_view(request, exception=None):
    return render(request, "system/error_page.html", {"title": "Достпу к странице запрещен", "status": 403})


def custom_bad_request_view(request, exception=None):
    return render(request, "system/error_page.html", {"title": "Неправильный запрос", "status": 400})


class SignUpView(views.View):
    def get(self, request):
        return render(request, 'registration/sign_up.html', {'form': SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = form.cleaned_data['is_admin']  # Устанавливаем флаг is_staff для администраторов
            user.set_password(form.cleaned_data['password1'])  # Убедитесь, что пароль хэшируется правильно
            user.save()

            # Добавляем пользователя в группу администраторов, если он регистрируется как администратор
            if user.is_staff:
                group = Group.objects.get(name='Администраторы')
                user.groups.add(group)

            login(request, user)
            if user.is_staff:
                return redirect('test_list')  # Перенаправляем администратора на страницу со списком тестов
            else:
                return redirect('home')  # Перенаправляем обычного пользователя на главную страницу
        return render(request, 'registration/sign_up.html', {'form': form})


class AccessTestView(views.View):
    def get(self, request):
        form = TestAccessForm()
        return render(request, 'quiz/access_test.html', {'form': form})

    def post(self, request):
        form = TestAccessForm(request.POST)
        if form.is_valid():
            access_key = form.cleaned_data['access_key']
            test = get_object_or_404(Test, access_key=access_key)
            now = timezone.now()
            if test.start_time <= now <= test.end_time:
                return redirect('test_description', test_id=test.id)
            return render(request, 'quiz/access_test.html', {'error_message': 'Тест недоступен в данное время'})


class TestDescriptionView(mixins.LoginRequiredMixin, views.View):
    def get(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        question_count = Question.objects.filter(test=test).count()
        max_score = sum(question.score for question in Question.objects.filter(test=test))
        return render(request, 'quiz/test_description.html', {
            'test': test,
            'question_count': question_count,
            'max_score': max_score,
        })


class TestView(mixins.LoginRequiredMixin, views.View):
    def get(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        questions = Question.objects.filter(test=test)
        return render(request, 'quiz/take_test.html', {'test': test, 'questions': questions})

    def post(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        questions = Question.objects.filter(test=test)
        score = 0
        for question in questions:
            correct_answers = question.answer_set.filter(is_correct=True)
            if question.type == 1:
                selected_answer = request.POST.get(f'question_{question.id}')
                correct_answer = correct_answers.values_list('id', flat=True).first()
                if selected_answer and int(selected_answer) == correct_answer:
                    score += question.score
            elif question.type == 2:
                selected_answers = set(map(int, request.POST.getlist(f'question_{question.id}')))
                correct_answers = set(correct_answers.values_list('id', flat=True))
                if selected_answers and selected_answers == correct_answers:
                    score += question.score
            elif question.type == 3:
                entered_answer = request.POST.get(f'question_{question.id}').lower()
                correct_answers = set(correct_answers.values_list('text', flat=True))
                if entered_answer and entered_answer in correct_answers:
                    score += question.score
        UserTestResult.objects.create(user=request.user, test=test, score=score)
        return render(request, 'quiz/test_result.html', {'score': score, 'pass_score': test.pass_score})


class UserTestResultsView(mixins.LoginRequiredMixin, views.View):
    def get(self, request):
        user_results = UserTestResult.objects.filter(user=request.user)
        return render(request, 'quiz/user_results.html', {'results': user_results})


class TestCreateView(UserPassesTestMixin, views.View):
    template_name = 'quiz/test_form.html'
    success_url = reverse_lazy('test_list')

    def test_func(self):
        return self.request.user.is_staff and self.request.user.groups.filter(name='Администраторы').exists()

    def get(self, request):
        form = TestForm()
        return render(request, self.template_name, {'form': form, 'action': 'Создать'})

    def post(self, request):
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.access_key = secrets.token_urlsafe(8)  # Генерируем уникальный ключ доступа
            test.created_by = request.user  # Устанавливаем автора теста
            test.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'action': 'Создать'})


class TestUpdateView(UserPassesTestMixin, views.View):
    template_name = 'quiz/test_form.html'
    success_url = reverse_lazy('test_list')

    def test_func(self):
        return self.request.user.is_staff and self.request.user.groups.filter(name='Администраторы').exists()

    def get(self, request, pk):
        test = get_object_or_404(Test, pk=pk, created_by=request.user)
        form = TestForm(instance=test)
        return render(request, self.template_name, {'form': form, 'action': 'Редактировать'})

    def post(self, request, pk):
        test = get_object_or_404(Test, pk=pk, created_by=request.user)
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'action': 'Редактировать'})


class TestDeleteView(UserPassesTestMixin, views.View):
    success_url = reverse_lazy('test_list')

    def test_func(self):
        return self.request.user.is_staff and self.request.user.groups.filter(name='Администраторы').exists()

    def get(self, request, pk):
        test = get_object_or_404(Test, pk=pk, created_by=request.user)
        test.delete()
        return redirect(self.success_url)


class TestListView(UserPassesTestMixin, views.View):
    template_name = 'quiz/test_list.html'

    def test_func(self):
        return self.request.user.is_staff and self.request.user.groups.filter(name='Администраторы').exists()

    def get(self, request):
        tests = Test.objects.filter(created_by=request.user)
        return render(request, self.template_name, {'tests': tests})


class TestStatisticsView(UserPassesTestMixin, views.View):
    template_name = 'quiz/test_statistics.html'

    def test_func(self):
        return self.request.user.is_staff and self.request.user.groups.filter(name='Администраторы').exists()

    def get(self, request, test_id):
        test = get_object_or_404(Test, id=test_id, created_by=request.user)
        results = UserTestResult.objects.filter(test=test)
        return render(request, self.template_name, {'test': test, 'results': results})


class QuestionListView(UserPassesTestMixin, views.View):
    template_name = 'quiz/question_list.html'

    def test_func(self):
        return self.request.user.is_staff and self.request.user.groups.filter(name='Администраторы').exists()

    def get(self, request, test_id):
        test = get_object_or_404(Test, id=test_id, created_by=request.user)
        questions = Question.objects.filter(test=test).prefetch_related('answers')
        return render(request, self.template_name, {'test': test, 'questions': questions})


class QuestionGetView(views.View):
    def get(self, request, test_id, question_id):
        question = get_object_or_404(Question, id=question_id)
        data = {
            'id': question.id,
            'text': question.text,
            'score': question.score,
            'type': question.type,
        }
        return JsonResponse(data)


class QuestionCreateView(views.View):
    def post(self, request, test_id):
        text = request.POST.get('text')
        score = request.POST.get('score')
        question_type = request.POST.get('type')
        new_question = Question.objects.create(
            text=text,
            score=score,
            type=question_type,
            test_id=test_id
        )
        return JsonResponse({'newQuestionText': new_question.text})


class QuestionUpdateView(views.View):
    def post(self, request, test_id, question_id):
        question = get_object_or_404(Question, question_id=question_id)
        question.text = request.POST.get('text')
        question.score = request.POST.get('score')
        question.question_type = request.POST.get('type')
        question.save()
        return JsonResponse({'updatedText': question.text})


class QuestionDeleteView(views.View):
    def post(self, request, test_id, question_id):
        question = get_object_or_404(Question, question_id=question_id)
        question.delete()
        return JsonResponse({'success': True})


class AnswerGetView(views.View):
    def get(self, request, test_id, question_id, answer_id):
        answer = get_object_or_404(Answer, id=answer_id)
        data = {
            'id': answer.id,
            'text': answer.text,
            'is_correct': answer.is_correct,
        }
        return JsonResponse(data)


class AnswerAddView(views.View):
    def post(self, request, test_id, question_id):
        text = request.POST.get('text')
        is_correct = request.POST.get('is_correct') == 'True'
        question = get_object_or_404(Question, id=question_id)
        new_answer = Answer.objects.create(
            text=text,
            is_correct=is_correct,
            question=question
        )
        return JsonResponse({'id': new_answer.id, 'text': new_answer.text, 'is_correct': new_answer.is_correct})


class AnswerUpdateView(views.View):
    def post(self, request, test_id, question_id, answer_id):
        answer = get_object_or_404(Answer, id=answer_id)
        text = request.POST.get('text')
        is_correct = request.POST.get('is_correct') == 'True'
        answer.text = text
        answer.is_correct = is_correct
        answer.save()
        return JsonResponse({'id': answer.id, 'text': answer.text, 'is_correct': answer.is_correct})


class AnswerDeleteView(views.View):
    def post(self, request, test_id, question_id, answer_id):
        answer = get_object_or_404(Answer, id=answer_id)
        answer.delete()
        return JsonResponse({'success': True})

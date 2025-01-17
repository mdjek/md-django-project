from django import views
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, mixins
from django.utils import timezone
from quiz.models import Test, Question, UserTestResult
from quiz.forms import SignUpForm, TestAccessForm


class UserTestResultsView(mixins.LoginRequiredMixin, views.View):
    def get(self, request):
        user_results = UserTestResult.objects.filter(user=request.user)
        return render(request, 'quiz/user_results.html', {'results': user_results})


class SignUpView(views.View):
    def get(self, request):
        return render(request, 'registration/sign_up.html', {'form': SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
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
                return redirect('take_test', test_id=test.id)
            return render(request, 'quiz/access_test.html', {'error_message': 'Тест недоступен в данное время'})


class TestView(views.View):
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
                selected_answer = int(request.POST.get(f'question_{question.id}'))
                correct_answer = correct_answers.values_list('id', flat=True).first()
                if selected_answer and selected_answer == correct_answer:
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


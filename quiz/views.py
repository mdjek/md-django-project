from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.utils import timezone
from quiz.models import Test, Question, Answer, UserTestResult
from quiz.forms import SignUpForm, TestAccessForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def enter_test(request):
    if request.method == 'POST':
        form = TestAccessForm(request.POST)
        if form.is_valid():
            access_key = form.cleaned_data['access_key']
            test = get_object_or_404(Test, access_key=access_key)
            now = timezone.now()
            if test.start_time <= now <= test.end_time:
                return redirect('take_test', test_id=test.id)
            else:
                return render(request, 'quiz/error.html', {'message': 'Тест недоступен в данное время.'})
    else:
        form = TestAccessForm()
    return render(request, 'quiz/enter_test.html', {'form': form})

def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = Question.objects.filter(test=test)
    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_answer = request.POST.get(f'question_{question.id}')
            if selected_answer:
                answer = Answer.objects.get(id=selected_answer)
                if answer.is_correct:
                    score += question.score
        UserTestResult.objects.create(user=request.user, test=test, score=score)
        return render(request, 'quiz/result.html', {'score': score, 'pass_score': test.pass_score})
    return render(request, 'quiz/take_test.html', {'test': test, 'questions': questions})

    def result(request, test_id):
        test = Test.objects.get(id=test_id)
        score = 100 
        return render(request, 'quiz/result.html', {'test': test, 'score': score})
# -*- coding: utf-8 -*-
# 
#  views.py
#  kanji_tester
#  
#  Created by Lars Yencken on 2008-06-13.
#  Copyright 2008-06-13 Lars Yencken. All rights reserved.
# 

from django.shortcuts import render
from django.conf import settings
from django.utils import timezone

from drill import models as drill_models
from drill import stats
from drill.views import TestSetForm
from user_model import models as usermodel_models
from user_profile.decorators import profile_required
from tutor import study_list


def welcome(request):
    """An alternative to the dashboard for users who aren't logged in."""

    return render(request, 'tutor/welcome.html', {'project_name': settings.PROJECT_NAME})


@profile_required
def dashboard(request):
    """Render the dashboard interface."""    
    context = {}
    charts = study_list.get_performance_charts(request.user)
    if charts:
        context['has_results'] = True
        context['stats'] = stats.get_stats(request.user)
        word_chart, kanji_chart = charts
        word_chart.set_size('260x200')
        kanji_chart.set_size('260x200')
        context['word_chart'] = word_chart
        context['kanji_chart'] = kanji_chart
    else:
        context['has_results'] = False

    return render(request, 'tutor/dashboard.html', context)


@profile_required
def test_user(request):
    """Run a test for the user."""
    context = {'syllabus': request.user.profile.syllabus}

    if 'test_set_id' not in request.POST:
        n_questions = settings.QUESTIONS_PER_SET
        start_time = timezone.now()  # time.time()
        if request.method == 'POST' and 'n_questions' in request.POST:
            n_questions = int(request.POST['n_questions'])
        test_set = drill_models.TestSet.from_user(request.user, n_questions=n_questions)
        form = TestSetForm(test_set)
        time_taken = timezone.now() - start_time  # time.time() - start_time
        context['time_taken'] = time_taken
    else:
        if request.method != 'POST':
            raise Exception("expected a POST form")
        test_set_id = int(request.POST['test_set_id'])
        test_set = drill_models.TestSet.objects.get(pk=test_set_id)
        form = TestSetForm(test_set, request.POST)

    context['test_set'] = test_set
    context['form'] = form
    context['syllabus'] = request.user.profile.syllabus

    return render(request, 'tutor/test_set.html', context)


@profile_required
def study(request):
    """Study the mistakes made in a test set."""
    context = {}
    if request.method != 'POST' or 'test_set_id' not in request.POST:
        test_set = drill_models.TestSet.get_latest_completed(request.user)
    else:
        test_set_id = int(request.POST['test_set_id'])
        test_set = drill_models.TestSet.objects.get(id=test_set_id)
        
    failed_responses = test_set.responses.filter(option__is_correct=False)
    failed_questions = test_set.questions.filter(
            response__in=failed_responses)

    failed_kanji = failed_questions.filter(pivot_type='k')
    kanji_set = set(o['pivot_id'] for o in failed_kanji.values('pivot_id'))
    partial_kanji = usermodel_models.PartialKanji.objects.filter(
            id__in=kanji_set)

    failed_lexemes = failed_questions.filter(pivot_type='w')
    lexeme_set = set(o['pivot_id'] for o in failed_lexemes.values('pivot_id'))
    partial_lexemes = usermodel_models.PartialLexeme.objects.filter(
            id__in=lexeme_set)

    context['partial_kanji'] = partial_kanji
    context['partial_lexemes'] = partial_lexemes
    context['all_correct'] = not partial_kanji and not partial_lexemes
    
    return render(request, 'tutor/study.html', context)


def about(request):
    return render(request, 'tutor/about.html', {'project_name': settings.PROJECT_NAME})



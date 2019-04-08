# -*- coding: utf-8 -*-
# 
#  admin.py
#  kanji_tester
#  
#  Created by Lars Yencken on 2008-09-30.
#  Copyright 2008 Lars Yencken. All rights reserved.
# 

from django.contrib import admin

from . import models


class OptionInline(admin.StackedInline):
    model = models.MultipleChoiceOption
    extra = 1


class MultipleChoiceAdmin(admin.ModelAdmin):
    list_display = ('pivot', 'pivot_type', 'pivot_id', 'question_type', 'question_plugin', 'annotation')
    list_filter = ('pivot_type', 'question_type')
    search_fields = ('pivot',)
    inlines = [OptionInline]


class QuestionPluginAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_adaptive')
    list_filter = ('is_adaptive',)


admin.site.register(models.QuestionPlugin, QuestionPluginAdmin)


class MultipleChoiceResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'option', 'timestamp')
    list_filter = ('timestamp',)


class MultipleChoiceOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'value', 'annotation', 'is_correct')
    list_filter = ('is_correct',)


class TestSetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'accuracy', 'start_time', 'end_time', 'set_type')
    list_filter = ('end_time', 'set_type')


admin.site.register(models.MultipleChoiceQuestion, MultipleChoiceAdmin)
admin.site.register(models.MultipleChoiceResponse, MultipleChoiceResponseAdmin)
admin.site.register(models.MultipleChoiceOption, MultipleChoiceOptionAdmin)
admin.site.register(models.TestSet, TestSetAdmin)

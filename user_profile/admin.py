# -*- coding: utf-8 -*-
#
#  admin.py
#  kanji_tester
# 
#  Created by Lars Yencken on 13-11-2008.
#  Copyright 2008 Lars Yencken. All rights reserved.
#

from django.contrib import admin

from user_profile import models


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'syllabus', 'first_language', 'second_languages')
    list_filter = ('first_language', 'syllabus')


admin.site.register(models.UserProfile, UserProfileAdmin)

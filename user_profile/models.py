# -*- coding: utf-8 -*-
#
#  models.py
#  kanji_tester
# 
#  Created by Lars Yencken on 13-11-2008.
#  Copyright 2008 Lars Yencken. All rights reserved.
#

"""
Models for the user_profile app.
"""

from django.db import models
from django.contrib.auth.models import User

from user_model.models import Syllabus


class UserProfile(models.Model):
    """Basic model of the user's kanji knowledge and study goals."""
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE)
    first_language = models.CharField(max_length=100)
    second_languages = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"UserProfile for {self.user.username}"

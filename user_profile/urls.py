# -*- coding: utf-8 -*-
#
#  urls.py
#  kanji_tester
# 
#  Created by Lars Yencken on 13-11-2008.
#  Copyright 2008 Lars Yencken. All rights reserved.
#

from django.conf.urls import url

from user_profile.views import create_profile

urlpatterns = (  # patterns('kanji_tester.user_profile.views',
    url(r'^$', create_profile, name='userprofile_profile'),
)

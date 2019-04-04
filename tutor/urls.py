# -*- coding: utf-8 -*-
# 
#  urls.py
#  kanji_tester
#  
#  Created by Lars Yencken on 2008-06-23.
#  Copyright 2008 Lars Yencken. All rights reserved.
# 

from django.conf.urls import url

from tutor.views import dashboard, welcome, test_user, study, about

urlpatterns = (
    url(r'^$', dashboard, name='tutor_dashboard'),
    url(r'^welcome/$', welcome, name='tutor_welcome'),
    url(r'^test/$', test_user, name='tutor_testuser'),
    url(r'^study/$', study, name='tutor_study'),
    url(r'^about/$', about, name='tutor_about'),
)

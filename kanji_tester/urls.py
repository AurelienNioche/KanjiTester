# -*- coding: utf-8 -*-
# 
#  urls.py
#  kanji_tester
#  
#  Created by Lars Yencken on 2008-06-13.
#  Copyright 2008-06-13 Lars Yencken. All rights reserved.
# 

from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth.urls

import django_registration.backends.activation.urls

import tutor.urls
import user_profile.urls
import analysis.urls

# import settings


admin.autodiscover()

urlpatterns = (
        url(r'^admin/', admin.site.urls),
        url(r'^accounts/', include(django_registration.backends.activation.urls)),
        url(r'^accounts/', include(django.contrib.auth.urls)),
        url(r'', include(tutor.urls)),
        url(r'^profile/', include(user_profile.urls)),
        url(r'^analysis/', include(analysis.urls)),
    )

# from kanji_tester.views import media
# # Optional static view for debugging and testing.
# if not settings.DEPLOYED:
#     urlpatterns += (
#             url(r'^static/', media, name='static'),
#         )

# Add the default pages.
# urlpatterns += (
#         url(r'', include('tutor.urls')),
#         url(r'^profile/', include('user_profile.urls')),
#         url(r'^analysis/', include('kanji_tester.analysis.urls')),
#     )

# urlpatterns = #patterns(*base_patterns)

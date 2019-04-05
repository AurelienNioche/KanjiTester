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

import settings

from kanji_tester.views import media

admin.autodiscover()

urlpatterns = (
        url(r'^admin/', include(admin.site.urls)),
        url(r'^accounts/', include('django_registration.backends.activation.urls')),
        url(r'^accounts/', include('django.contrib.auth.urls')),
    )

# Optional static view for debugging and testing.
if not settings.DEPLOYED:
    urlpatterns += (
            url(r'^static/', media, name='static'),
        )

# Add the default pages.
urlpatterns += (
        url(r'', include('tutor.urls')),
        url(r'^profile/', include('user_profile.urls')),
        url(r'^analysis/', include('kanji_tester.analysis.urls')),
    )

# urlpatterns = #patterns(*base_patterns)

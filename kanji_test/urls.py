# -*- coding: utf-8 -*-
# 
#  urls.py
#  kanji_test
#  
#  Created by Lars Yencken on 2008-06-13.
#  Copyright 2008-06-13 Lars Yencken. All rights reserved.
# 

from django.conf.urls import url, include
from django.contrib import admin

import settings

from kanji_test.views import media

admin.autodiscover()

urlpatterns = (#'',
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
        url(r'', include('kanji_test.tutor.urls')),
        url(r'^profile/', include('kanji_test.user_profile.urls')),
        url(r'^analysis/', include('kanji_test.analysis.urls')),
    )

# urlpatterns = #patterns(*base_patterns)

# -*- coding: utf-8 -*-
# 
#  views.py
#  kanji_tester
#  
#  Created by Lars Yencken on 2008-07-03.
#  Copyright 2008 Lars Yencken. All rights reserved.
# 

import django.views.static

from kanji_tester import settings

def media(request):
    "A static view which renders static. Not to be used in deployment."
    return django.views.static.serve(
            request,
            request.path[len(settings.MEDIA_URL):],
            document_root=settings.MEDIA_ROOT,
        )

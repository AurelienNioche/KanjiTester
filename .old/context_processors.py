# -*- coding: utf-8 -*-
# 
#  kanji_tester/context_processors.py
#  kanji_tester
#  
#  Created by Lars Yencken on 2008-06-23.
#  Copyright 2008 Lars Yencken. All rights reserved.
# 

from kanji_tester import settings

def basic_vars(request):
    """Provides some basic variables for the request."""
    return {
        'media_url':        settings.MEDIA_URL,
        'admin_media_url':  settings.ADMIN_MEDIA_PREFIX,
        'project_name':     settings.PROJECT_NAME,
        'analytics_code':   settings.GOOGLE_ANALYTICS_CODE,
    }

# -*- coding: utf-8 -*-
#
#  build.py
#  kanji_tester
# 
#  Created by Lars Yencken on 18-09-2008.
#  Copyright 2008 Lars Yencken. All rights reserved.
#

"""
A command to run the build method of all apps.
"""
from functools import reduce

from django.core.management.base import BaseCommand
from django.conf import settings 

import consoleLog


_log = consoleLog.default


class Command(BaseCommand):
    help = "Builds all required static database tables."
    requires_model_validation = True

    def handle(self, *args, **options):
        apps_with_build = []
        for app_path in settings.INSTALLED_APPS:
            base_module = __import__(app_path)
            app_module = reduce(getattr, app_path.split('.')[1:], base_module)
            if hasattr(app_module, 'build'):
                apps_with_build.append((app_path, app_module))

        _log.start('Building kanji_tester', n_steps=len(apps_with_build))
        for app_path, app_module in apps_with_build:
            app_module.build()
        _log.finish()

# vim: ts=4 sw=4 sts=4 et tw=78:

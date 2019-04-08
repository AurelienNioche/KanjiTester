# -*- coding: utf-8 -*-
#
#  admin.py
#  checksum
# 
#  Created by Lars Yencken on 09-11-2008.
#  Copyright 2008 Lars Yencken. All rights reserved.
#

"""
Admin interface for the checksum app.
"""

from django.contrib import admin

from checksum import models


class ChecksumAdmin(admin.ModelAdmin):
    list_display = ('tag', 'value')


admin.site.register(models.Checksum, ChecksumAdmin)

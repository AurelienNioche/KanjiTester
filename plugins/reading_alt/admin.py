# -*- coding: utf-8 -*-
#
#  admin.py
#  reading_alt
# 
#  Created by Lars Yencken on 09-11-2008.
#  Copyright 2008 Lars Yencken. All rights reserved.
#

from django.contrib import admin

from plugins.reading_alt import models


class KanjiReadingAdmin(admin.ModelAdmin):
    list_display = ('condition', 'symbol', 'alternations', 'pdf', 'cdf')
    search_fields = ('condition', 'alternations')


admin.site.register(models.KanjiReading, KanjiReadingAdmin)


class ReadingAlternationAdmin(admin.ModelAdmin):
    list_display = ('value', 'code', 'probability')


admin.site.register(models.ReadingAlternation, ReadingAlternationAdmin)

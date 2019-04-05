# -*- coding: utf-8 -*-
#
#  lang_middleware.py
#  kanji_tester
# 
#  Created by Lars Yencken on 18-04-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
"""

from cjktools import scripts


class TagLanguageMiddleware(object):
    def __init__(self, get_response):
        self.japanese_scripts = {scripts.Script.Katakana, scripts.Script.Hiragana, scripts.Script.Kanji}
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        response = self.get_response(request)
        # if response.status_code != 200:
        #     return response
        #
        # if not response.get('Content-Type', '').startswith('text/html'):
        #     return response
        #
        # content = response.content.decode('utf8')
        # if not scripts.script_types(content).intersection(self.japanese_scripts):
        #     return response
        #
        # parts = []
        # for part in scripts.script_boundaries(content):
        #     if scripts.script_type(part) in self.japanese_scripts:
        #         print("JPN", part)
        #         parts.append('<span lang="ja" xml:lang="ja">%s</span>' % part)
        #     else:
        #         print("NON-JPN", part)
        #         if u'\n' in part:
        #             print("EMPTY")
        #         else:
        #             print("NON EMPTY")
        #             parts.append(part)
        #
        # response.content = u''.join(parts).encode('utf8')
        # print("9999")
        # print(response)
        return response

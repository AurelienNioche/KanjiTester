# # -*- coding: utf-8 -*-
# #
# #  __init__.py
# #  kanji_tester
# #
# #  Created by Lars Yencken on 2008-09-29.
# #  Copyright 2008 Lars Yencken. All rights reserved.
# #
#
# """
# A broad interface for test questions and their database management.
# """
#
# from django.conf import settings
#
#
# def load_plugins(plugin_set=settings.DRILL_PLUGINS):
#     """
#     Returns a list of plugin instances from the set given, defaulting to
#     all the plugins which are available.
#     """
#     plugins = []
#     for plugin_path in plugin_set:
#         import_path = plugin_path.split('.')
#         plugin_class_name = import_path.pop()
#         module = __import__('.'.join(import_path))
#         for sub_module in import_path[1:]:
#             module = getattr(module, sub_module)
#         plugin_class = getattr(module, plugin_class_name)
#         plugins.append(plugin_class())
#
#     return plugins

# -*- coding: utf-8 -*-
# 
#  plugin_api.py
#  kanji_tester
#  
#  Created by Lars Yencken on 2008-10-24.
#  Copyright 2008 Lars Yencken. All rights reserved.
# 

# from itertools import imap, izip

from functools import reduce

import consoleLog
from cjktools import scripts

from kanji_tester import settings
from user_model import models


class UpdateError(Exception):
    pass


# class UserModelPlugin(object):
#     """
#     A plugin which provides one or more prior distributions across a form
#     of user error.
#     """
#
#     def init_priors(self):
#         """Initialises the prior distributions that this plugin provides."""
#         raise Exception('not implemented')
#
#     def update(self, _response):
#         """Updates this error model from a user's response."""
#         raise Exception('not implemented')


class SegmentedSeqPlugin:  # (UserModelPlugin):
    """
    A plugin which uses annotated segments in its options. Requires its
    class to define a "dist_name" attribute, and to define segment annotations
    for all questions and their options.

    Questions should be annotated with segments from the domain of error
    distribution conditions, and options annotated with segments from the 
    domain of error distribution symbols, or outcomes.
    """
    def update(self, response):
        """Update our error model from a user's response."""
        error_dist = models.ErrorDist.objects.get(user=response.user, tag=self.dist_name)
        question = response.question
        base_segs = question.annotation.split(u'|')
        response_segs = response.option.annotation.split(u'|')
        distractor_sets = list(map(set, zip(
                *[o['annotation'].split('|')
                for o in question.multiplechoicequestion.options.values(
                        'annotation')
                if o['annotation'] != response.option.annotation]
            )))
        assert len(base_segs) == len(response_segs) == len(distractor_sets)

        for base_seg, response_seg, distractor_segs in zip(base_segs, response_segs, distractor_sets):
            if scripts.script_types(base_seg) != scripts.Script.Kanji:
                continue
            sub_dist = models.ProbDist.from_query_set(
                    error_dist.density.filter(condition=base_seg))
            e = settings.UPDATE_EPSILON

            try:
                m = max(map(sub_dist.__getitem__, distractor_segs)) + e
                existing_score = sub_dist[response_seg]
            except KeyError:
                raise UpdateError(
                    u'for user %s, dist %s, response %d: no entry for %s|%s' % (
                            response.user.username,
                            self.dist_name,
                            response.id,
                            response_seg,
                            base_seg,
                    ))

            if m > existing_score:
                sub_dist[response_seg] = m
                sub_dist.normalise()
                sub_dist.save_to(error_dist.density, condition=base_seg)
        return


_cached_plugins = None


def load_plugins():
    """
    Loads the list of plugin classes specified in USER_MODEL_PLUGINS in the
    project settings.

    >>> from kanji_tester import settings
    >>> len(load_plugins()) == len(settings.USER_MODEL_PLUGINS)
    True
    """
    global _cached_plugins

    if not _cached_plugins:
        plugin_classes = []
        for plugin_path in settings.USER_MODEL_PLUGINS:
            path_parts = plugin_path.split('.')
            base_module = __import__('.'.join(path_parts[:-1]))
            plugin_class = reduce(getattr, path_parts[1:], base_module)
            plugin_classes.append(plugin_class)
        _cached_plugins = dict((c.dist_name, c()) for c in plugin_classes)

    return _cached_plugins


def load_priors(syllabus, force=False):
    """Loads the prior distributions represented by each plugin."""
    log = consoleLog.default
    log.start('Loading prior distributions', n_steps=2)

    log.log('Loading plugins')
    plugins = load_plugins()

    log.start('Initialising prior distributions', n_steps=len(plugins))
    for plugin_obj in plugins.values():
        plugin_obj.init_priors(syllabus, force=force)
    log.finish()

    log.finish()


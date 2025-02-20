# -*- coding: utf-8 -*-
#
#  __init__.py
#  kanji_tester
#
#  Created by Lars Yencken on 2008-06-21.
#  Copyright 2008-06-21 Lars Yencken. All rights reserved.
#

"""
Plugin for visual similarity.
"""

import consoleLog
from simplestats.comb import iunique_pairs
# from cjktools.errors import DomainError
from django.core.exceptions import ObjectDoesNotExist

from user_model import models as usermodel_models, plugin_api as user_model_api
from drill import plugin_api as drill_api, support
from lexicon import models as lexicon_models
from kanji_tester import settings

from plugins.visual_similarity.metrics.stroke import StrokeEditDistance
import plugins.visual_similarity.threshold_graph as threshold_graph

# _default_metric_name = 'stroke edit distance'
_log = consoleLog.default


class VisualSimilarity(user_model_api.SegmentedSeqPlugin):
    dist_name = "kanji' | kanji"

    def init_priors(self, syllabus, force=False):
        prior_dist, created = syllabus.priordist_set.get_or_create(
            tag=self.dist_name)
        if not created:
            if not force:
                # Keep the existing distribution.
                return

            prior_dist.priorpdf_set.all().delete()

        _log.start("Building %s dist" % self.dist_name, n_steps=3)

        _log.log('Fetching syllabus kanji')
        kanji_set = set([k_row.kanji for k_row in
                         lexicon_models.Kanji.objects.filter(
                             partialkanji__syllabus=syllabus)])

        _log.log('Generating similarity graph ', new_line=False)
        graph = self._build_graph(kanji_set)

        _log.log('Storing priors')
        self._store_graph(graph, prior_dist)

        _log.finish()

    def _build_graph(self, kanji_set):
        metric = StrokeEditDistance()  # metrics.strmetric_library[_default_metric_name]
        graph = threshold_graph.ThresholdGraph(settings.MAX_GRAPH_DEGREE)
        ignore_set = set()
        for kanji_a, kanji_b in consoleLog.with_progress(iunique_pairs(kanji_set), 100):
            if kanji_a in ignore_set or kanji_b in ignore_set:
                continue

            try:
                weight = metric(kanji_a, kanji_b)
            except Exception as e:
                kanji = str(e)
                ignore_set.add(kanji)
                continue

            graph.connect(kanji_a, kanji_b, weight)

        for kanji in kanji_set:
            graph.connect(kanji, kanji, 0.0)

        return graph

    def _store_graph(self, graph, prior_dist):
        for label, edge_seq in graph._heaps.items():
            total_weight = 0.0
            for weight, neighbour_label in edge_seq:
                total_weight += 1.0 - weight

            cdf = 0.0
            for weight, neighbour_label in edge_seq:
                pdf = (1.0 - weight) / total_weight
                cdf += pdf
                prior_dist.density.create(
                    condition=label,
                    symbol=neighbour_label,
                    pdf=pdf,
                    cdf=cdf,
                )


class VisualSimilarityDrills(drill_api.MultipleChoiceFactoryI):
    """Distractors are sampled from the user error distribution."""
    question_type = 'gp'
    requires_kanji = True
    uses_dist = "kanji' | kanji"
    is_adaptive = True
    verbose_name = 'visual similarity'

    def get_kanji_question(self, partial_kanji, user):
        self.error_dist = usermodel_models.ErrorDist.objects.get(user=user,
                                                                 tag=self.uses_dist)

        kanji_row = partial_kanji.kanji
        kanji = kanji_row.kanji
        question = self.build_question(
            pivot=kanji,
            pivot_id=partial_kanji.id,
            pivot_type='k',
            stimulus=kanji_row.gloss,
        )
        self._add_distractors(question, user)
        return question

    def get_word_question(self, partial_lexeme, user):
        lexeme = partial_lexeme.lexeme
        try:
            surface = partial_lexeme.random_kanji_surface
        except ObjectDoesNotExist:
            raise drill_api.UnsupportedItem(partial_lexeme)

        # Assume the first sense is the dominant sense
        gloss = lexeme.sense_set.get(is_first_sense=True).gloss

        question = self.build_question(
            pivot=surface,
            pivot_id=partial_lexeme.id,
            pivot_type='w',
            stimulus=gloss,
        )
        self._add_distractors(question, user)
        return question

    def _add_distractors(self, question, user):
        """
        Builds distractors for the question with appropriate annotations so
        that we can easily update the error model afterwards.

        Note that the segments used here are simplistic, one per character,
        since the richer GP segments need not be supported by this error
        distribution.
        """
        error_dist = user.errordist_set.get(tag=self.uses_dist)
        pivot = question.pivot
        segments = list(pivot)  # Simple segments
        if question.pivot_type == 'w':
            distractors, annotation_map = support.build_word_options(
                segments, error_dist, exclude_set={pivot})
        else:
            distractors, annotation_map = support.build_kanji_options(
                question.pivot, error_dist, exclude_set={pivot})
        annotation_map[pivot] = u'|'.join(segments)
        question.add_options(distractors, question.pivot,
                             annotation_map=annotation_map)
        question.annotation = u'|'.join(segments)
        question.save()

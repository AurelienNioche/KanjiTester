# Move in reading_alt.py

# """
# A django app for modelling kanji reading alternations.
# """
#
# import consoleLog
# from django.db import connection
# from django.conf import settings
#
# from user_model import models as usermodel_models, plugin_api as usermodel_api
# from drill import plugin_api as drill_api, support
# from util.probability import ProbDist
# from lexicon import models as lexicon_models
#
# _log = consoleLog.default
#
#
# class KanjiReadingModel(usermodel_api.SegmentedSeqPlugin):
#     dist_name = 'reading | kanji'
#
#     def __init__(self):
#         pass
#
#     def init_priors(self, syllabus, force=False):
#         _log.start('Building %s dist' % self.dist_name, nSteps=4)
#
#         # Ensure the reading database is pre-built
#         import reading_database
#         reading_database.ReadingDatabase.build()
#
#         prior_dist, created = usermodel_models.PriorDist.objects.get_or_create(
#             tag=self.dist_name, syllabus=syllabus)
#         if not created:
#             if force:
#                 prior_dist.density.all().delete()
#             else:
#                 return
#
#         _log.log('Fetching syllabus kanji')
#         kanji_set = self._fetch_syllabus_kanji(syllabus)
#
#         _log.log('Storing readings')
#         self._import_readings(prior_dist, kanji_set)
#
#         _log.start('Padding reading lists', nSteps=1)
#         self._pad_readings(prior_dist)
#         _log.finish()
#
#         _log.finish()
#
#     def _fetch_syllabus_kanji(self, syllabus):
#         kanji_set = set(row['kanji'] for row in \
#                         lexicon_models.Kanji.objects.filter(
#                             partialkanji__syllabus=syllabus
#                         ).values('kanji')
#                         )
#         return kanji_set
#
#     def _import_readings(self, prior_dist, kanji_set):
#         "Copies the reading database directly into an prior distribution."
#         cursor = connection.cursor()
#         quote_name = connection.ops.quote_name
#         fields_a = ', '.join(map(quote_name, ['dist_id', 'condition',
#                                               'symbol', 'pdf', 'cdf']))
#         fields_b = ', '.join(map(quote_name, ['condition', 'symbol', 'pdf',
#                                               'cdf']))
#         fields_c = quote_name('condition')
#         cursor.execute("""
#                 INSERT INTO user_model_priorpdf (%s)
#                 SELECT %s as `dist_id`, %s
#                 FROM reading_alt_kanjireading
#                 WHERE %s IN (%s)
#             """ % (fields_a, str(prior_dist.id), fields_b, fields_c,
#                    u', '.join(u'"%s"' % k for k in kanji_set)))
#         cursor.execute('COMMIT')
#         return
#
#     def _pad_readings(self, prior_dist):
#         """
#         Once the reading distribution has been copied over, we still have the
#         problem that there may not be enough erroneous readings to meet the
#         minimum number of distractors we wish to generate.
#
#         To circumvent this problem, we pad with random distractors.
#         """
#         _log.log('Padding results ', newLine=False)
#         conditions = set(o['condition'] for o in \
#                          prior_dist.density.all().values('condition'))
#         for (condition,) in consoleLog.withProgress(conditions):
#             exclude_set = set(
#                 o.reading for o in \
#                 lexicon_models.KanjiReading.objects.filter(
#                     kanji__kanji=condition)
#             )
#             n_stored = prior_dist.density.filter(condition=condition).exclude(
#                 symbol__in=exclude_set).count()
#
#             sub_dist = ProbDist.from_query_set(prior_dist.density.filter(
#                 condition=condition))
#             exclude_set.update(sub_dist.keys())
#             n_needed = settings.MIN_TOTAL_DISTRACTORS - n_stored
#             min_prob = min(sub_dist.values()) / 2
#             while n_needed > 0:
#                 for row in lexicon_models.KanjiReadingProb.sample_n(n_needed):
#                     if row.symbol not in exclude_set:
#                         sub_dist[row.symbol] = min_prob
#                         exclude_set.add(row.symbol)
#                         n_needed -= 1
#
#                     if n_needed == 0:
#                         break
#
#             sub_dist.normalise()
#             sub_dist.save_to(prior_dist.density, condition=condition)
#
#         return
#
#
# class ReadingAlternationQuestions(drill_api.MultipleChoiceFactoryI):
#     """
#     A factory for reading questions using FOKS-style reading alternations.
#     Questions are annotated with their grapheme segments, and potential
#     answers (Options) are annotated with their phoneme segments.
#     """
#     question_type = 'pr'
#     requires_kanji = True
#     uses_dist = 'reading | kanji'
#     description = 'A reading alternation model is used to generate' \
#                   ' distractors.'
#     is_adaptive = True
#     verbose_name = 'reading alternations'
#
#     def get_word_question(self, partial_lexeme, user):
#         "See parent."
#         try:
#             alignment = partial_lexeme.alignments.order_by('?')[0]
#         except IndexError:
#             raise drill_api.UnsupportedItem(partial_lexeme)
#
#         error_dist = usermodel_models.ErrorDist.objects.get(user=user,
#                                                             tag=self.uses_dist)
#         surface = alignment.surface.surface
#
#         # [339] Include homographs in real reading set
#         exclude_set = set([
#             r.reading for r in lexicon_models.LexemeReading.objects.filter(
#                 lexeme__surface_set__surface=surface)
#         ])
#
#         answer_reading = alignment.reading.reading
#         pivot = alignment.surface.surface
#         assert answer_reading in exclude_set
#         question = self.build_question(
#             pivot=pivot,
#             pivot_id=partial_lexeme.id,
#             pivot_type='w',
#             stimulus=surface,
#         )
#         alignment_obj = alignment.alignment_obj
#         distractors, annotation_map = support.build_word_options(
#             alignment_obj.g_segs, error_dist,
#             exclude_set=exclude_set)
#         annotation_map[answer_reading] = u'|'.join(alignment_obj.p_segs)
#         question.add_options(distractors, answer_reading,
#                              annotation_map=annotation_map)
#         question.annotation = u'|'.join(alignment_obj.g_segs)
#         question.save()
#         return question
#
#     def get_kanji_question(self, partial_kanji, user):
#         "See parent."
#         error_dist = usermodel_models.ErrorDist.objects.get(user=user,
#                                                             tag=self.uses_dist)
#         exclude_set = set(row['reading'] for row in \
#                           partial_kanji.kanji.reading_set.values('reading'))
#         answer = partial_kanji.reading_set.order_by('?').values(
#             'reading')[0]['reading']
#         kanji = partial_kanji.kanji.kanji
#         question = self.build_question(
#             pivot=kanji,
#             pivot_id=partial_kanji.id,
#             pivot_type='k',
#             stimulus=kanji,
#         )
#         distractors, annotation_map = support.build_kanji_options(
#             kanji, error_dist, exclude_set=exclude_set,
#             adaptive=self.is_adaptive)
#         annotation_map[answer] = answer  # No segments
#         question.add_options(distractors, answer,
#                              annotation_map=annotation_map)
#         question.annotation = kanji  # No segments
#         question.save()
#         return question
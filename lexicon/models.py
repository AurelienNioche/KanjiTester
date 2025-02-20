# -*- coding: utf-8 -*-
# 
#  models.py
#  kanji_tester
#  
#  Created by Lars Yencken on 2008-06-21.
#  Copyright 2008-06-21 Lars Yencken. All rights reserved.
# 

import random
from os import path

from django.db import models
from cjktools.resources import kanjidic
from cjktools import scripts

from util import probability
from util import models as prob_models

from kanji_tester import settings


class Lexeme(models.Model):
    """A single word or phrase."""
    def _get_random_sense(self):
        return self.sense_set.order_by('?')[0]
    random_sense = property(_get_random_sense)
    
    def first_sense(self):
        return self.sense_set.get(is_first_sense=True)
    first_sense = property(first_sense)
        
    def __unicode__(self):
        return '/'.join(
                s.surface for s in self.surface_set.order_by('surface')
            ) + ' [%d]' % self.id
    
    def __hash__(self):
        return hash(self.id)


class LexemeSurface(models.Model):
    """A surface rendering of the word."""
    lexeme = models.ForeignKey(Lexeme, related_name='surface_set', on_delete=models.CASCADE)
    surface = models.CharField(max_length=60, db_index=True)
    priority_codes = models.CharField(
        blank=True, max_length=60, null=True,
        help_text='Any annotations the original dictionary provided')
    has_kanji = models.BooleanField(
        help_text='Does this entry contain any kanji characters?')
    in_lexicon = models.BooleanField(
        default=True,
        help_text='Is this part of the original lexicon?')

    class Meta:
        unique_together = (('lexeme', 'surface'),)

    @staticmethod
    def sample():
        while True:
            surface = LexemeSurfaceProb.sample().symbol
            matches = LexemeSurface.objects.filter(surface=surface)
            if len(matches) > 0:
                return random.choice(matches)

    def _get_prob(self):
        return LexemeSurfaceProb.objects.get(symbol=self.surface)
    prob = property(_get_prob)
    
    def __unicode__(self):
        return self.surface


class LexemeReading(models.Model):
    """A valid pronunciation for a lexeme."""
    lexeme = models.ForeignKey(Lexeme, related_name='reading_set', on_delete=models.CASCADE)
    reading = models.CharField(max_length=60, db_index=True)
    priority_codes = models.CharField(blank=True, max_length=60, null=True)

    def __unicode__(self):
        return self.reading

    class Meta:
        unique_together = (('lexeme', 'reading'),)


class LexemeSense(models.Model):
    """A word sense."""
    lexeme = models.ForeignKey(Lexeme, related_name='sense_set', on_delete=models.CASCADE)
    gloss = models.CharField(max_length=500)
    is_first_sense = models.BooleanField()

    class Meta:
        # XXX Uniqueness constraint doesn't work due in mysql due to length of
        #   gloss field.
        # unique_together = (('lexeme', 'gloss'),)
        pass

    def __unicode__(self):
        return self.gloss

    @classmethod
    def sample_n(cls, n):
        surface_set = LexemeSurfaceProb.sample_n(n)
        return cls.objects.filter(
            lexeme__surface_set__in=surface_set,
            is_first_sense=True)


class KanjiProb(prob_models.Prob):
    """A frequency distribution over kanji."""
    _freq_dist_file = path.join(
        settings.DATA_DIR, 'corpus',
        'jp_char_corpus_counts.gz')

    def _get_kanji(self):
        return Kanji.objects.get(kanji=self.symbol)
    kanji = property(_get_kanji)

    class Meta(prob_models.Prob.Meta):
        verbose_name = 'probability of kanji'
        verbose_name_plural = 'distribution of kanji'

    @classmethod
    def initialise(cls):
        dist = probability.FreqDist.from_file(cls._freq_dist_file)
        cls.from_dist(dist)
    
    @classmethod
    def sample_kanji(cls):
        return Kanji.objects.get(kanji=cls.sample().symbol)


class KanjiReadingProb(prob_models.Prob):
    """A frequency distribution of kanji pronunciations."""
    _freq_dist_file = path.join(
        settings.DATA_DIR, 'corpus', 'kanji_reading_counts')
        
    class Meta(prob_models.Prob.Meta):
        verbose_name = 'probability of reading'
        verbose_name_plural = 'distribution of readings'
    
    @classmethod
    def initialise(cls):
        cond_dist = probability.ConditionalFreqDist.from_file(
                cls._freq_dist_file, format='packed')
        dist = cond_dist.without_condition()
        cls.from_dist(dist)


class KanjiReadingCondProb(prob_models.CondProb):
    """
    A conditional frequency distribution over kanji readings.
    
    >>> KanjiReadingCondProb.initialise()
    >>> KanjiReadingCondProb.objects.filter(
    ...     condition=unicode('日', 'utf8')).count()
    45
    """
    _freq_dist_file = path.join(
        settings.DATA_DIR, 'corpus', 'kanji_reading_counts')
    
    def _get_kanji_reading(self):
        return KanjiReading.objects.get(kanji=self.condition, reading=self.symbol)
    kanji_reading = property(_get_kanji_reading)
    
    class Meta(prob_models.CondProb.Meta):
        verbose_name = 'probability of reading given kanji'
        verbose_name_plural = 'distribution of readings given kanji'
    
    @classmethod
    def fetch_dist(cls, condition):
        return probability.FixedProb((o.symbol, o.pdf) for o in
                                     cls.objects.filter(condition=condition).all())
    
    @classmethod
    def initialise(cls):
        dist = probability.ConditionalFreqDist.from_file(
            cls._freq_dist_file,
            format='packed')
        cls.from_dist(dist)
    
    @classmethod
    def sample_kanji_reading(cls):
        row = cls.sample()
        return KanjiReading.objects.get(
            kanji=row.condition,
            reading=row.symbol)

    def __unicode__(self):
        return u'%s /%s/ %g' % (
                self.condition,
                self.symbol,
                self.pdf,
            )


class LexemeSurfaceProb(prob_models.Prob):
    """A probability distribution over lexical surface items."""
    _freq_dist_file = path.join(settings.DATA_DIR, 'corpus', 'jp_word_corpus_counts.gz')

    class Meta(prob_models.Prob.Meta):
        verbose_name = 'probability of lexeme surface'
        verbose_name_plural = 'distribution of lexeme surfaces'

    def __unicode__(self):
        return u'%s %g' % (self.symbol, self.pdf)

    @classmethod
    def initialise(cls):
        dist = probability.FreqDist.from_file(cls._freq_dist_file)
        cls.from_dist(dist)


class LexemeReadingProb(prob_models.CondProb):
    """A probability distribution over lexeme readings."""    
    class Meta(prob_models.CondProb.Meta):
        verbose_name = 'probability of reading given lexeme'
        verbose_name_plural = 'distribution of readings given lexeme'
    
    def __unicode__(self):
        return u'%s /%s/ %g' % (self.condition, self.symbol, self.pdf)
    
    @classmethod
    def initialise(cls):
        # TODO Find a data source for lexeme reading probabilities.
        pass


class Kanji(models.Model):
    """A single unique kanji and its meaning."""
    kanji = models.CharField(max_length=3, primary_key=True)
    gloss = models.CharField(max_length=200)
    
    def _get_prob(self):
        return KanjiProb.objects.get(symbol=self.kanji)
    prob = property(_get_prob)
    
    class Meta:
        ordering = ['kanji']
        verbose_name_plural = 'kanji'

    def __unicode__(self):
        return self.kanji
    
    @classmethod
    def initialise(cls):
        KanjiReading.objects.all().delete()
        Kanji.objects.all().delete()
        kjd = kanjidic.Kanjidic.get_cached()
        max_gloss_len = [f for f in cls._meta.fields if f.name == 'gloss'][0].max_length
        for entry in kjd.values():
            truncated_gloss = ', '.join(entry.gloss)[:max_gloss_len]
            kanji = Kanji(kanji=entry.kanji, gloss=truncated_gloss)
            kanji.save()
            for reading in cls._clean_readings(entry.on_readings):
                kanji.reading_set.create(reading=reading, reading_type='o')
            for reading in cls._clean_readings(entry.kun_readings):
                kanji.reading_set.create(reading=reading, reading_type='k')
        return
    
    @staticmethod
    def _clean_readings(reading_list):
        return set(
                scripts.to_hiragana(r.split('.')[0]) for r in reading_list
            )


class KanjiReading(models.Model):
    """A reading for a single kanji."""
    kanji = models.ForeignKey(Kanji, related_name='reading_set', on_delete=models.CASCADE)
    reading = models.CharField(max_length=21, db_index=True)
    READING_TYPES = (('o', 'on'), ('k', 'kun'))
    reading_type = models.CharField(max_length=1, choices=READING_TYPES)
    
    def _get_prob(self):
        return KanjiReadingCondProb.objects.get(
            condition=self.kanji,
            symbol=self.reading)
    prob = property(_get_prob)
    
    class Meta:
        unique_together = (('reading', 'kanji', 'reading_type'),)
        ordering = ['kanji', 'reading']

    def __unicode__(self):
        return u'%s /%s/' % (self.kanji, self.reading)


def initialise():
    Kanji.initialise()
    KanjiProb.initialise()
    KanjiReadingProb.initialise()
    KanjiReadingCondProb.initialise()
    LexemeSurfaceProb.initialise()
    LexemeReadingProb.initialise()

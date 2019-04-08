# -*- coding: utf-8 -*-
#
#  alignment.py
#  kanji_tester
# 
#  Created by Lars Yencken on 06-11-2008.
#  Copyright 2008 Lars Yencken. All rights reserved.
#

"""
Resouces for parsing and utilising alignments.
"""

# from itertools import zip

# from cjktools.common import sopen
from cjktools.scripts import contains_script, Script


class FormatError(Exception):
    pass


_gp_sep = ':'
_seg_sep = '|'


class Alignment:
    __slots__ = ('g_segs', 'p_segs')

    def __init__(self, g_segs, p_segs):
        if len(g_segs) != len(p_segs):
            raise ValueError('segment lengths must match')

        self.g_segs = g_segs
        self.p_segs = p_segs

    @property
    def grapheme(self):
        return u''.join(self.g_segs)

    @property
    def phoneme(self):
        return u''.join(self.p_segs)

    def has_kanji(self):
        return contains_script(Script.Kanji, self.grapheme)

    def __len__(self):
        return len(self.g_segs)

    def __iter__(self):
        for item in zip(self.g_segs, self.p_segs):
            yield item

    def __next__(self):
        return self

    def __str__(self):
        return ' '.join(
                [_seg_sep.join(self.g_segs), _seg_sep.join(self.p_segs)],
            )
    
    @classmethod
    def from_line(cls, line):
        parts = line.rstrip().split(_gp_sep)
        try:
            entry, alignment = parts
            g_segs, p_segs = alignment.split()
        except ValueError:
            raise FormatError(line)

        return cls(g_segs.split(_seg_sep), p_segs.split(_seg_sep))

    def to_line(self):
        return _gp_sep.join([self.entry_form(), self.short_form()])

    def entry_form(self):
        return f'{self.grapheme} {self.phoneme}'

    def short_form(self):
        return f'{_seg_sep.join(self.g_segs)} {_seg_sep.join(self.p_segs)}'

    @classmethod
    def from_short_form(cls, short_alignment):
        g_segs, p_segs = short_alignment.split()
        g_segs = g_segs.split(_seg_sep)
        p_segs = p_segs.split(_seg_sep)
        return Alignment(g_segs, p_segs)


class AlignedFile:
    def __init__(self, filename):
        self._alignments = []

        i_stream = open(filename, 'r')
        for i, line in enumerate(i_stream):
            if line.lstrip().startswith('#'):
                continue
            try:
                self._alignments.append(Alignment.from_line(line))
            except:
                raise FormatError('on line %d of %s' % (i + 1, filename))
        i_stream.close()

    def __next__(self):
        return self

    def __iter__(self):
        return iter(self._alignments)

    def __len__(self):
        return len(self._alignments)

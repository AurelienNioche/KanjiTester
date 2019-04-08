# -*- coding: utf-8 -*-
# 
#  consoleLog.py
#  consoleLog
#  
#  Created by Lars Yencken on 2008-06-12.
#  Copyright 2008 Lars Yencken. All rights reserved.
# 

"""
A simple logging module which allows hierarchical logging without centralized
control.

>>> log = ConsoleLogger()
>>> log.start('ABC', n_steps=3)
ABC
>>> log.log('A')
├─ A
>>> log.log('B')
├─ B
>>> log.log('C')
└─ C
>>> log.finish()
"""


import sys

_default_encoding = 'utf8'


class ConsoleLogger(object):
    """
    A console logging object, which can optionally be given an output stream
    which it prints to, defaulting to stdout.
    """
    def __init__(self, output=None, trim=78):  # , encoding=_default_encoding):
        self.oStream = open(output, 'w') if output else sys.stdout  # codecs.getwriter(encoding)(output or sys.stdout)
        self.logStack = []
        self.trim = trim

    def start(self, message, n_steps=None):
        """
        Starts a new hierarchical logging section. Every call to start() must
        be later matched by a call to finish().
        """
        self.log(message)
        self.logStack.append(_SectionPadding(n_steps=n_steps))
        return

    def log(self, message, new_line=True):
        """
        Logs a message, with an optional newline. The most common case for
        not using the newline is for subsequent use of a progress bar.
        """
        if self.logStack:
            padding = []
            for levelLogger in self.logStack[:-1]:
                padding.append(levelLogger.get_intermediate_padding())
            padding.append(self.logStack[-1].get_current_padding())
        else:
            padding = ''
        o_line = ''.join(padding) + f'{message}'   # % (u''.join(padding), message)
        if self.trim and len(o_line) > self.trim:
            o_line = o_line[:self.trim - 3] + '...'

        if new_line:
            print(o_line, file=self.oStream)
            self.oStream.flush()
        else:
            print(o_line, file=self.oStream, end=' ')

    def space(self):
        if self.logStack:
            padding = []
            for levelLogger in self.logStack:
                padding.append(levelLogger.get_intermediate_padding())
            padding = u''.join(padding)
        else:
            padding = u''
        print(padding, file=self.oStream)

    def finish(self, message="Done"):
        """
        Ends a hierarchical logging section which was previously created using
        start().
        """
        padding = []
        for levelLogger in self.logStack[:-1]:
            padding.append(levelLogger.get_intermediate_padding())
        last = self.logStack.pop()
        padding.append(last.get_last_padding())
        if last.needs_finish():
            print(u"%s%s" % (u''.join(padding), message), file=self.oStream)


class _SectionPadding(object):
    """
    A manager for the amount of padding needed for any given log line, as well
    as any embellishments needed to indicate hierarchy.
    """
    def __init__(self, n_steps=None):
        """Private constructor used internally."""
        self.nSteps = n_steps
        self.currentStep = 0

    def get_intermediate_padding(self):
        if self.currentStep == self.nSteps:
            return u'   '
        else:
            return u'│  '

    def get_current_padding(self):
        self.currentStep += 1
        if self.currentStep == self.nSteps:
            return u'└─ '
        else:
            return u'├─ '

    def needs_finish(self):
        return self.currentStep != self.nSteps

    @staticmethod
    def get_last_padding():
        return u'└─ '

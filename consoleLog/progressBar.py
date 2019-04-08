# -*- coding: utf-8 -*-
# 
#  progressBar.py
#  consoleLog
#  
#  Created by Lars Yencken on 2008-06-12.
#  Copyright 2008-06-12 Lars Yencken. All rights reserved.
#

"""
A simple console progress bar, with support for iterator wrapping.
"""


import sys
import time

# import io
import consoleLog.shellColor as shellColor
import consoleLog.slot as slot


_currentBar = None


class IllegalNestingError(Exception):
    pass


def with_progress(seq, mod_value=1, size=None, force=False):
    """
    A wrapper for sequence which adds a progress bar.
    """
    global _currentBar
    if _currentBar:
        raise IllegalNestingError("can't nest progress bars")

    progress = ProgressBar()
    if size is None:
        if hasattr(seq, '__len__'):
            progress.start(len(seq))
        elif force:
            seq = list(seq)
            progress.start(len(seq))
        else:
            raise (ValueError, "seq has no __len__ method")
    else:
        progress.start(size)

    _currentBar = progress

    count = 0
    for item in seq:
        yield item
        count += 1
        if count % mod_value == 0:
            progress.update(count)

    progress.finish()

    _currentBar = None
    return


def tick():
    """
    Indicate activity in the current progress bar.
    """
    global _currentBar

    if _currentBar is not None:
        _currentBar.tick()
    return


class ProgressBar:
    """A progress bar which gets printed to stdout."""
    def __init__(self, string_size=20):
        """Creates a new instance, setting the size as needed."""

        self._slot = slot.Slot()
        self._stringSize = string_size
        self._count = 0
        self._totalCount = None
        self._lastRotation = 0
        self._startTime = None

        self._rotation = ['/', '-', '\\', '|']
        self._numRotations = len(self._rotation)

        return

    def reset(self):
        """Resets the progress bar to initial conditions."""
        self._count = 0
        self._totalCount = None
        self._lastRotation = 0
        self._startTime = None
    
    def start(self, total_count):
        """
        Starts the progress bar. This will be the first output from the
        bar. At this stage it needs the total count so that it can
        calculate percentages.

        @param total_count: The count which represents 'finished'.
        """
        assert self._count == 0, "Progress bar already started, call reset()"
        assert total_count > 0, "Progress bar needs a non-zero total count"
        self._totalCount = total_count
        progress_line = '[' + shellColor.color('/', 'red') + (self._stringSize-1)*' ' + ']   0%'
        self._slot.update(progress_line)
        self._startTime = time.time()

    def update(self, count):
        """
        Updates the progress bar with the current count. This is useful
        to call even if the count has not increased, since it provides
        visual feedback to the user that the process is active.

        @param count: The current count
        """
        count = int(count)
        self._count = count
        if count < 0 or count > self._totalCount:
            raise (Exception, 'Bad count for progress bar')

        n = int((count * self._stringSize) / self._totalCount)
        percent = int((100*count) / self._totalCount)
        m = self._stringSize - n - 1  # subtract one for the rotating char

        self._lastRotation = (self._lastRotation + 1) % self._numRotations
        if percent < 100:
            rot_char = self._rotation[self._lastRotation]
        else:
            rot_char = ''

        progress_line = '[' + shellColor.color(n*'-' + rot_char, 'red') + m*' ' + '] ' + str('%3d%%' % percent)
        self._slot.update(progress_line)

    def tick(self):
        """Perform a quick update."""
        self.update(self._count)

    def fractional(self, fraction):
        """Set a fractional percentage completion, e.g. 0.3333 -> 33%."""
        assert 0 <= fraction <= 1
        self.update(int(fraction * self._totalCount))
    
    def finish(self):
        """Fixes to 100% complete, and writes the time taken."""
        assert self._totalCount > 0, "Progress bar wasn't initialised"
        self.update(self._totalCount)

        time_taken = int(time.time() - self._startTime)
        (mins, secs) = divmod(time_taken, 60)
        if not mins:
            time_string = ' (%ds)' % secs
        else:
            (hours, mins) = divmod(mins, 60)
            if not hours:
                time_string = ' (%dm %ds)' % (mins, secs)
            else:
                time_string = ' (%dh %dm %ds)' % (hours, mins, secs)

        print(time_string, file=sys.stdout)


if __name__ == '__main__':
    for i in with_progress(range(100)):
        time.sleep(0.1)

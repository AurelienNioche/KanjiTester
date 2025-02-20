# -*- coding: utf-8 -*-
# 
#  io.py
#  consoleLog
#  
#  Created by Lars Yencken on 2008-06-12.
#  Copyright 2008-06-12 Lars Yencken. All rights reserved.
# 

"""
The sopen() convenience method for file handles.
"""

import sys
import codecs
import bz2
import gzip


def sopen(filename, mode='rb', encoding='utf8'):
    """
    Transparently uses compression on the given file based on file
    extension.

    @param filename: The filename to use for the file handle.
    @param mode: The mode to open the file in, e.g. 'r' for read, 'w' for
        write, 'a' for append.
    @param encoding: The encoding to use. Can be set to None to avoid
        using unicode at all.
    """
    read_mode = 'r' in mode
    if read_mode and 'w' in mode:
        raise (Exception, "Must be either read mode or write, but not both")

    if filename.endswith('.bz2'):
        stream = bz2.BZ2File(filename, mode)
    elif filename.endswith('.gz'):
        stream = gzip.GzipFile(filename, mode)
    elif filename == '-':
        if read_mode:
            stream = sys.stdin
        else:
            stream = sys.stdout
    else:
        stream = open(filename, mode)
    
    if encoding not in (None, 'byte'):
        if read_mode:
            return codecs.getreader(encoding)(stream)
        else:
            return codecs.getwriter(encoding)(stream)
    
    return stream

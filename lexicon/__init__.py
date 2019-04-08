# -*- coding: utf-8 -*-
# 
#  __init__.py
#  kanji_tester
#  
#  Created by Lars Yencken on 2008-06-21.
#  Copyright 2008-06-21 Lars Yencken. All rights reserved.
# 

"""
An application which provides basic and exact lexical access.
"""

# Dependencies


def build():
    from lexicon import load_lexicon
    load_lexicon.load_lexicon()

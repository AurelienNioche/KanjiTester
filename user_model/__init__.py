# -*- coding: utf-8 -*-
# 
#  __init__.py
#  kanji_tester
#  
#  Created by Lars Yencken on 2008-10-24.
#  Copyright 2008 Lars Yencken. All rights reserved.
# 

"""
All aspects of user proficiency and error modeling.
"""

# Dependencies


def build():
    from user_model import add_syllabus
    add_syllabus.add_all_syllabi()

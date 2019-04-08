#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
#  testProbability.py
#  kanji_tester
#  
#  Created by Lars Yencken on 2008-09-28.
#  Copyright 2008 Lars Yencken. All rights reserved.
# 

import os
import unittest
import tempfile

# from cjktools.common import sopen

from util import probability

# def suite():
#     testSuite = unittest.TestSuite((
#             unittest.makeSuite(CondFreqDistTest),
#         ))
#     return testSuite


class CondFreqDistTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_from_packed_file(self):
        test_filename = tempfile.mktemp()
        o_stream = open(test_filename, 'w')
        print('dog bark:9,pee:1', file=o_stream)
        print('cat meow:10', file=o_stream)
        o_stream.close()
        self._check_file(test_filename, 'packed')

    def test_from_row_file(self):
        test_filename = tempfile.mktemp()
        o_stream = open(test_filename, 'w')
        print('dog bark 9', file=o_stream)
        print('dog pee 1', file=o_stream)
        print('cat meow 10', file=o_stream)
        o_stream.close()
        self._check_file(test_filename, 'row')
        
    def _check_file(self, filename, format):
        try:
            cond_dist = probability.ConditionalFreqDist.from_file(
                    filename, format=format)
            self.assertEqual(set(cond_dist.conditions()), {'dog', 'cat'})
            self.assertEqual(set(cond_dist['dog'].samples()),
                             {'bark', 'pee'})
            self.assertEqual(cond_dist['dog']['bark'], 9)
            self.assertEqual(cond_dist['dog']['pee'], 1)
            self.assertEqual(cond_dist['cat']['meow'], 10)
        except:
            if os.path.exists(filename):
                os.remove(filename)
            raise        

# if __name__ == '__main__':
#     unittest.main()

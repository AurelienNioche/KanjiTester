# -*- coding: utf-8 -*-
#
#  test_basic.py
#  simplestats
# 
#  Created by Lars Yencken on 10-04-2009.
#  Copyright 2009 Lars Yencken. All rights reserved.
#

import unittest
# import doctest

from simplestats import basic

#
#
# def suite():
#     testSuite = unittest.TestSuite((
#             unittest.makeSuite(BasicStatsTest),
#             doctest.DocTestSuite(basic),
#         ))
#     return testSuite


class BasicStatsTest(unittest.TestCase):
    def setUp(self):
        self.dataA = [1, 2, 3]
        self.meanA = 2.0
        self.stddevA = 1.0

        self.dataB = [-50.4, 30.2, 0.1, 4.327]
        self.meanB = -3.94325
        self.stddevB = 33.70824
        return

    def testMean(self):
        """
        Check that mean works as expected.
        """
        self.assertAlmostEqual(basic.mean(self.dataA), self.meanA, 5)
        self.assertAlmostEqual(basic.mean(self.dataB), self.meanB, 5)
        return

    def testBadStddev(self):
        """
        Check stddev on a list of length 0.
        """
        try:
            basic.stddev([])
        except:
            pass
        else:
            assert False, "Stddev didn't raise an exception on an empty list"

        return

    def testStddev(self):
        """
        Check that stddev works as expected.
        """
        self.assertAlmostEqual(basic.stddev(self.dataA), self.stddevA, 5)
        self.assertAlmostEqual(basic.stddev(self.dataB), self.stddevB, 5)
        return

    def testOnTuples(self):
        """
        Checks that methods also work on tuples.
        """
        self.assertAlmostEqual(basic.mean(tuple(self.dataA)), self.meanA, 5)
        self.assertAlmostEqual(basic.mean(tuple(self.dataB)), self.meanB, 5)
        self.assertAlmostEqual(basic.stddev(tuple(self.dataA)), self.stddevA, 5)
        self.assertAlmostEqual(basic.stddev(tuple(self.dataB)), self.stddevB, 5)
        return

    def testBasicStats(self):
        """
        Test that the basic stats method works.
        """
        meanA, stddevA = basic.basic_stats(self.dataA)
        self.assertAlmostEqual(meanA, basic.mean(self.dataA))
        self.assertAlmostEqual(stddevA, basic.stddev(self.dataA))
        return

    def tearDown(self):
        pass


# if __name__ == "__main__":
#     unittest.TextTestRunner(verbosity=1).run(suite())


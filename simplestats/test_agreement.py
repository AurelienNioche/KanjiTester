# -*- coding: utf-8 -*-
#
#  test_agreement.py
#  simplestats
# 
#  Created by Lars Yencken on 10-04-2009.
#  Copyright 2009 Lars Yencken. All rights reserved.
#

import unittest
# import doctest
from simplestats import agreement


#
# def suite():
#     testSuite = unittest.TestSuite((
#             unittest.makeSuite(KappaTest),
#             doctest.DocTestSuite(agreement)
#         ))
#     return testSuite
#


class KappaTest(unittest.TestCase):
    def setUp(self):
        self.dataA = [1, 2, 3, 4]
        self.dataB = [2, 3, 4, 5]

    def testHighKappa(self):
        """
        Tests a high kappa value
        """
        kappaVal = agreement.kappa(self.dataA, self.dataA)
        self.assertAlmostEqual(kappaVal, 1.0)
        return
    
    def testNoAgreement(self):
        """
        Tests the no agreement case.
        """
        kappaVal = agreement.kappa(self.dataA, self.dataB)
        self.assertAlmostEqual(kappaVal, -0.23076923076923078)
        return

    def testZeroKappa(self):
        kappaVal = agreement.kappa(self.dataA, [0,0,6,6])
        self.assertAlmostEqual(kappaVal, 0)
        return

    def tearDown(self):
        pass


# if __name__ == "__main__":
#     unittest.TextTestRunner(verbosity=1).run(suite())

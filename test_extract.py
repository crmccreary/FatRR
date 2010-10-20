import unittest
import sys, os
import extractMaxS

class Extract(unittest.TestCase):
    def test_1(self):
        N = extractMaxS.Nf(90.0, -0.5)
        self.assertAlmostEquals(N, 100000, -4)

def suite():
    suite1 = unittest.makeSuite(Extract)
    return unittest.TestSuite([suite1])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Extract)
    unittest.TextTestRunner(verbosity=2).run(suite)

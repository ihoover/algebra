import unittest
from qform import Qform

class TestQformStatic(unittest.TestCase):
    """
    Test static methods of Qform
    """
    
    def testIsReduced_false_bbig(self):
        self.assertFalse(Qform.isReduced(2,3,4))
    
    def testIsReduced_false_abig(self):
        self.assertFalse(Qform.isReduced(5,3,4))
    
    def testIsReduced_false_bneg(self):
        self.assertFalse(Qform.isReduced(5,-3,5))
    
    def testIsReduced_true(self):
        self.assertTrue(Qform.isReduced(3,2,5))
    
    def testReduced(self):
        (a,b,c) = (95, -87, 21)
        self.assertEqual(Qform.reduced(a,b,c), (5,-3,21))
    
    def testReduced_already_reduced(self):
        (a,b,c) = (1,1,2)
        self.assertEqual(Qform.reduced(a,b,c), (a,b,c))
    

import unittest
from qform import Qform, ClassGroup

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
    
    def testIsReduced_true_bzero(self):
        self.assertTrue(Qform.isReduced(5,0,5))
    
    def testIsReduced_true(self):
        self.assertTrue(Qform.isReduced(3,2,5))
    
    def testReduced(self):
        (a,b,c) = (95, -87, 21)
        self.assertEqual(Qform.reduced(a,b,c), (5,-3,21))
    
    def testReduced_already_reduced(self):
        (a,b,c) = (1,1,2)
        self.assertEqual(Qform.reduced(a,b,c), (a,b,c))


class TestQform(unittest.TestCase):
    
    def testInstantiate(self):
        qform = Qform(1,2,3)
    
    def testStr_allPos(self):
        q = Qform(1,0,1)
        self.assertNotIn('-', str(q))
    
    def testStr_neg(self):
        q = Qform(2,-1,3)
        self.assertIn('- 1', str(q))
    
    def testMulAbelian(self):
        q1 = Qform(4,4,17)
        q2 = Qform(5,-2,13)
        self.assertEqual(q1*q2, q2*q1)
    
    def testMul(self):
        q1 = Qform(4,4,17)
        q2 = Qform(5,-2,13)
        self.assertEqual(q1*q2, Qform(20,28,13))
    
    def testIdentity(self):
        for n in range(1,200):
            for form in ClassGroup.allReduced(-4*n):
                self.assertEqual(form*form.identity(), form)
            for form in ClassGroup.allReduced(-4*n + 1):
                self.assertEqual(form*form.identity(), form)
    
    def testInv(self):
        for n in range(1,200):
            for form in ClassGroup.allReduced(-4*n):
                self.assertEqual(form*form.inv(), form.identity())
            for form in ClassGroup.allReduced(-4*n + 1):
                self.assertEqual(form*form.inv(), form.identity())

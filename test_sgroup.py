import unittest
from sgroup import *

class Testmset(unittest.TestCase):
    """
    test multiplicative sets
    """
    def setUp(self):
        self.elements = [Perm((1,2,3)), Perm((1,3,2))]
        self.elements2 = [Perm((1,2)), Perm((1,3))]
        self.mset = mset(self.elements)
        self.mset2 = mset(self.elements2)
    
    def test_mul(self):
        """
        test multiplying on the right by something else.  I use permutaiton
        objects since for them multiplication is non-commutative.
        """
        
        mset12 = mset([el*Perm((1,2)) for el in self.elements])
        
        self.assertEqual(mset12, self.mset*Perm((1,2)))
    
    def test_rmul(self):
        """
        tests that right and left multiplication are in fact different
        """
        
        I2mset = mset([Perm((1,2))*el for el in self.elements])
        
        self.assertEqual(I2mset, Perm((1,2))*self.mset)
    
    def test_mul_iterable(self):
        """
        test multiplying by an iterable object
        """
        
        prod = mset([m1*m2 for m1 in self.elements for m2 in self.elements2])
        self.assertEqual(prod, self.mset*set(self.elements2))
    
    def test_rmul_iterable(self):
        """
        test multiplying by an iterable object
        """
        
        prod = mset([m2*m1 for m1 in self.elements for m2 in self.elements2])
        self.assertEqual(prod, set(self.elements2)*self.mset)


class TestSGroup(unittest.TestCase):
    """
    test the symmetric group
    """
    
    def test_init(self):
        s3 = mset([Perm(()), Perm((1,2)), Perm((1,3)), Perm((3,2)), Perm((1,2,3)), Perm((1,3,2))])
        self.assertEqual(SGroup(3).elements, s3)
    
    def test_init_8def(self):
        from math import factorial as fac
        self.assertEqual(len(SGroup(8).elements), fac(8))
    

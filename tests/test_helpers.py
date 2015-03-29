from algebra import *
import unittest

class Testmset(unittest.TestCase):
    """
    test multiplicative sets
    """
    def setUp(self):
        self.elements = [Perm((1,2,3))]
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
        test multiplying by a set
        """
        
        prod = mset([m1*m2 for m1 in self.elements for m2 in self.elements2])
        self.assertEqual(prod, self.mset*set(self.elements2))
    
    def test_rmul_iterable(self):
        """
        test multiplying by an iterable object
        """
        
        prod = mset([m2*m1 for m1 in self.elements for m2 in self.elements2])
        self.assertEqual(prod, set(self.elements2)*self.mset)

     
class Testlcm(unittest.TestCase):
    """
    test the lcm function for mulstiple integers
    """
    
    def setUp(self):
        
        self.p1 = 2
        self.p2 = 3
        self.p3 = 5
    
    def test_no_input(self):
        
        self.assertRaises(TypeError, lcm)
    
    def test_one_input(self):
        
        self.assertEqual(2,lcm(2))
        
    def test_2_inputs(self):
        
        self.assertEqual(6, lcm(self.p1, self.p2))
    
    def test_3_inputs(self):
        
        self.assertEqual(self.p1*self.p2*self.p3, lcm(self.p1, self.p2, self.p3))
    
    def test_4_inputs(self):
        """
        this one they are not all prime
        """
        
        self.assertEqual(30, lcm(2,3,5,6))

    
class TestGcd(unittest.TestCase):
    """
    test gcd function
    """
    
    def setUp(self):
        
        self.p1 = 2
        self.p2 = 3
        self.p3 = 5
    
    def test_no_input(self):
        
        self.assertRaises(TypeError, lcm)
    
    def test_one_input(self):
        
        self.assertEqual(2,gcd(2))
        
    def test_2_inputs_rel_composit(self):
        
        self.assertEqual(self.p1, gcd(self.p1, self.p2*self.p1))
    
    def test_2_inputs_rel_prime(self):
        
        self.assertEqual(1, gcd(self.p1, self.p2))
    
    def test_3_inputs_all_relprime(self):
        
        self.assertEqual(1, gcd(self.p1, self.p2, self.p3))
    
    def test_3_inputs_two_relprime(self):
        
        self.assertEqual(1, gcd(self.p1, self.p2, self.p3*self.p2))
    
    
    def test_3_inputs_all_relcomposit(self):

        self.assertEqual(self.p1, gcd(self.p1,self.p2*self.p1, self.p3*self.p1))

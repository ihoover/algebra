import unittest
from algebra import *

class TestGroup(unittest.TestCase):
    """
    Tests for the group class
    """
    
    def test_eq(self):
        g1 = Group([1])
        g2 = Group([1])
        
        self.assertEqual(g1, g2)
    
    def test_elements(self):
        elements = {0,1,2,3,4}
        bin_op = lambda x,y: (x+y)%5
        g = Group(elements, bin_op = bin_op)
        
        self.assertEqual(elements, g.elements)
    
    def test_elements_with_generation(self):
        generators = [2]
        bin_op = lambda x,y: (x+y)%7
        elements = {0,1,2,3,4,5,6}
        g = Group(generators, bin_op)
        
        self.assertEqual(g.elements, elements)
    
    def test_duplicate_generatotrs(self):
        generators = [2,2,2,3]
        bin_op = lambda x,y: (x+y)%7
        elements = {0,1,2,3,4,5,6}
        g = Group(generators, bin_op)
        
        self.assertEqual(g.elements, elements)
    
    def test_center_abelian(self):
        g = Group([1], (lambda x,y: (x+y)%7))
        
        self.assertEqual(g.elements, g.center)
    
    def test_s3(self):
        g = Group({Perm((1,2)), Perm((1,3)), Perm((3,2))})
        s3 = mset([Perm(()), Perm((1,2)), Perm((1,3)), Perm((3,2)), Perm((1,2,3)), Perm((1,3,2))])
        
        self.assertEqual(g.elements, s3)
    
    def test_trivial_center(self):
        g = Group({Perm((1,2)), Perm((1,3)), Perm((3,2))})

        self.assertEqual(g.center, {Perm(())})

    def test_center_G4(self):
        
        g = Group({Perm((1,2,3,4)), Perm(((1,4),(2,3)))})
        center = {Perm(()), Perm(((1,3),(2,4)))}
        
        self.assertEqual(g.center, center)

class TestSGroup(unittest.TestCase):
    """
    test the symmetric group
    """
    
    def test_init(self):
        s3 = mset([Perm(()), Perm((1,2)), Perm((1,3)), Perm((3,2)), Perm((1,2,3)), Perm((1,3,2))])
        self.assertEqual(SGroup(3).elements, s3)
    
    def test_init_7def(self):
        from math import factorial as fac
        n = 7
        self.assertEqual(len(SGroup(n).elements), fac(n))
    
    def test_init_error_string(self):
        self.assertRaises(TypeError, SGroup, 'd')
    
    def test_init_error_non_int(self):
        self.assertRaises(TypeError, SGroup, 5.4)

    def test_init_error_neg_int(self):
        self.assertRaises(TypeError, SGroup, -2)
    
    def test_trivial_center(self):
        g = SGroup(5)
        self.assertEqual(g.center, {Perm(())})

import unittest
from sgroup import *

class TestPermClassFunctions(unittest.TestCase):
    """
    Test Cases for the permutation class (not instance specific)
    """

    def test_validate_list_incomplete(self):
        """
        test that an incomplete (lacking 0 or 1) list fails
        """
        
        incomplete_list = [2,3]
        self.assertFalse(Perm.validate_list(incomplete_list))
    
    def test_validate_list_negative(self):
        """
        test that a negative entry fails
        """
        
        neg_list = [-2,1]
        self.assertFalse(Perm.validate_list(neg_list))
    
    def test_validate_list_nonint(self):
        """
        test that a negative entry fails
        """
        
        nonint_list = [2.0,1]
        self.assertFalse(Perm.validate_list(nonint_list))
    
    
    def test_validate_list_duplicate_elements(self):
        """
        test that duplicates cause it to fail
        """
        
        duplicate_list = [1,3,2,1]
        self.assertFalse(Perm.validate_list(duplicate_list))
    
    def test_validate_list_skip_elements(self):
        """
        test that skipe cause it to fail
        """
        
        skip_list = [1,3,2,5]
        self.assertFalse(Perm.validate_list(skip_list))
    
    def test_validate_list_empty(self):
        """
        tests that the empty lists evaluates as valid
        """
        self.assertTrue(Perm.validate_list([]))
        
    def test_validate_list_normal(self):
        """
        tests that a proper, non-empty, lists evaluates as valid
        """
        normal_list = [5,3,6,1,4,2]
        self.assertTrue(Perm.validate_list(normal_list))
    
    def test_format_list_empty(self):
        """
        test that [] becomes [0]
        """
        
        self.assertEqual([0], Perm.format_list([]))
    
    def test_format_list_identity(self):
        """
        tests that any identity list become [0]
        """
        
        l = [0,1,2,3,4]
        self.assertEqual([0], Perm.format_list(l))
    
    def test_format_list_minimal(self):
        """
        tests that any extra at the end is left off
        """
        
        l = [1,0,2,3,4]
        l1 = [1,0]
        self.assertEqual(l1, Perm.format_list(l))
    
    def test_format_list_normal(self):
        """
        test format a already formatted list does not change anything
        """
        l = [2,1,0]
        self.assertEqual(l, Perm.format_list(l))
    
    def test_format_list_decrease(self):
        """
        tests that lists not containing 0 are decreased
        """
        originalList = [1,3,2]
        decreasedList = [0,2,1]
        self.assertEqual(decreasedList, Perm.format_list(originalList))
    
    def test_make_cycle(self):
        """
        test turning a permuted list into its list representation
        """
        
        cycles = ((1,2,3),)
        l = [1,2,0]
        
        self.assertEqual(cycles, Perm.make_cycles(l))
    
    def test_make_cycle_identity(self):
        """
        test the cycle maker on the identity permutation
        """
        
        l = [0]
        cycles = ((1,),)
        
        self.assertEqual(cycles, Perm.make_cycles(l))
    
    def test_make_cycle_double(self):
        """
        test with multiple cycles
        """
        l = [1,0,3,2]
        cycles = ((1,2),(3,4))
        
        self.assertEqual(cycles, Perm.make_cycles(l))
    
    def test_make_cycle_unmoved(self):
        """
        test that unmoved elements are dropped
        """
        l = [0,1,3,2]
        cycles = ((3,4),)

        self.assertEqual(cycles, Perm.make_cycles(l))
    
    def test_make_list(self):
        """
        test making single cycle into permuted list
        """
        
        cycle = ((1,2,3),)
        l = [1,2,0]
        
        self.assertEqual(l, Perm.make_list(cycle))
    
    def test_make_list_identity(self):
        """
        test that identity permutation is handled properly
        """
        
        cycle = ((1,),)
        l = [0]
        
        self.assertEqual(l, Perm.make_list(cycle))
    
    def test_make_list_incoplete(self):
        """
        test that permutation of only some of the elements is handled properly
        """
        
        cycle = ((4,5),)
        l = [0,1,2,4,3]
        
        self.assertEqual(l, Perm.make_list(cycle))
        
    def test_make_list_multiple(self):
        """
        test that permutation with multiple cycles is handled properly
        """
        
        cycle = ((1,2), (3,4))
        l = [1,0,3,2]
        
        self.assertEqual(l, Perm.make_list(cycle))
    
    def test_make_list_multiple2(self):
        """
        this time the cycles overlap
        """
        cycle = ((1,2), (1,2,3))
        #(2,3)
        l = [0,2,1]
        
        self.assertEqual(l, Perm.make_list(cycle))
    
    def test_make_list_multiple3(self):
        """
        this time the cycles overlap, a few more
        """
        cycle = ((1,2), (1,2,3), (1,2,3,4))
        #(1,3,4)
        l = [2,1,3,0]
        
        self.assertEqual(l, Perm.make_list(cycle))
    
    def test_validate_cycle_non_int(self):
        """
        test validate_cycle with non integer cycle
        """
        
        cycle = ('f', 2)
        self.assertFalse(Perm.validate_cycle(cycle))
    
    def test_validate_cycle_repeat(self):
        """
        test validate cycle with a repeated element  of the cycle
        """
        
        cycle = (1, 2, 1)
        self.assertFalse(Perm.validate_cycle(cycle))
    
    def test_validate_cycle_nonpositive(self):
        """
        test validate cycle with non-positive cycle elements
        """
        
        cycle = (1, 2, -1)
        self.assertFalse(Perm.validate_cycle(cycle))


class TestPermInit(unittest.TestCase):
    """
    test cases that are instance specific
    """
    
    def test_init_list(self):
        """
        test creating a permutaiton with a list
        """
        l = [0,1,3,2]
        cycle = ((3,4),)
        p = Perm(l)
        
        self.assertEqual(p.list, l)
        self.assertEqual(p.cycles, cycle)
        
    def test_init_cycle(self):
        """
        test creating a permutaiton with a cycle
        """
        l = [0,1,3,2]
        cycle = ((3,4),)
        p = Perm(cycle)
        
        self.assertEqual(p.list, l)
        self.assertEqual(p.cycles, cycle)
    
    def test_init_intcycle(self):
        """
        test creating a permutaiton with a cycle (just one)
        """
        
        l = [0,1,3,2]
        cycle0 = (3,4)
        cycle = ((3,4),)
        p = Perm(cycle0)
        
        self.assertEqual(p.list, l)
        self.assertEqual(p.cycles, cycle)
    
    def test_init_list_error(self):
        """
        test creating a permutaiton with a list that should cause an error
        """
        l = [0,1,3,'2']
        cycle = ((3,4),)
        self.assertRaises(TypeError, Perm, l)
    
    def test_init_cycle_error(self):
        """
        test creating a permutaiton with a cycle that should cause an error
        """
        cycle = ((3,4),2)
        self.assertRaises(TypeError, Perm, cycle)
    
    def test_init_perm(self):
        """
        test that it just copies the permutation object
        """
        p = Perm(((1,2,3),))
        q = Perm(p)
        
        self.assertEqual(p.cycles, q.cycles)
        self.assertEqual(q.list, p.list)
        self.assertFalse(p is q)
        self.assertFalse(p.list is q.list)
    
    def test_init_error(self):
        """
        test that it typeerrors on wrong type of input
        """
        
        self.assertRaises(TypeError, Perm, 'hello')


class TestPermCall(unittest.TestCase):
    """
    test calling the permutation.
    """
    def setUp(self):
        """
        create basic permutations to call
        """
        
        self.id = Perm([])
        self.perm1 = Perm(((1,2,3),))

    def test_call_simple(self):
        """
        test on basic permutation
        """
        l = [1,2,3]
        permuted = [2,3,1]
        
        self.assertEqual(permuted, self.perm1(l))       
    
    def test_call_bigger(self):
        """
        test that calling a small permutation on a big list works
        """
        
        l = [1,2,3,4,5,6,7,8]
        permuted = [2,3,1,4,5,6,7,8]
        
        self.assertEqual(permuted, self.perm1(l))       
    
    def test_call_identity(self):
        """
        test that calling the identity permutaiton works
        """
        
        l = [1,2,3]
        
        self.assertEqual(l, self.id(l))
    
    def test_call_tuple(self):
        """
        test using a tuple
        """
        
        t = (1,2,3)
        t2 = (2,3,1)
        
        self.assertEqual(t2, self.perm1(t))
    
    def test_call_string(self):
        """
        test ermuting a string
        """
        
        s = 'hello'
        s1 = 'elhlo'
        
        self.assertEqual(s1, self.perm1(s))
        

class TestPermEq(unittest.TestCase):
    """
    test permutation equality
    """
    def setUp(self):
        self.p1 = Perm(((1,2),))
    
    def test_eq_2perms_eq(self):
        p2 = Perm(((2,1),))
        
        self.assertEqual(self.p1,p2)
    
    def test_eq_list(self):
        
        self.assertEqual(self.p1, [1,0])
    
    def test_eq_2perms_neq(self):
        p2 = Perm([1,3,2])
        
        self.assertNotEqual(self.p1, p2)
    
    def test_eq_error(self):
        self.assertRaises(TypeError, self.p1.__eq__, 'hello')


class TestPermMul(unittest.TestCase):
    """
    test permutation multiplication
    """
    
    def test_mul(self):
        p1 = Perm(((1,2),))
        p2 = Perm(((1,2,3),))
        p3 = Perm(((2,3),))
        
        self.assertEqual(p1*p2, p3)
    
    def test_mul_error(self):
        p1 = Perm((1,2))
        p2 = Perm((1,2,3))
        p3 = Perm((2,3))
        
        self.assertRaises(TypeError, p1.__mul__, 'hello')

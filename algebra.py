from abc import ABCMeta, abstractmethod
import itertools

def gcd(m,n):
	if n==0:
		return m
	r = m%n
	return(gcd(n,r))

def lcm(*args):
    def lcm_short(a,b):
        return a*b/gcd(a,b)
    
    if len(args) == 0:
        raise TypeError("Must supply at least 1 integer.")
    
    if len(args) == 1:
        return args[0]
    
    else:
        return reduce(lcm_short,args)

class Element(object):
    """
    Abstract base class for implementing an algebraic element
    """
    
    __metaclass__ = ABCMeta
    @abstractmethod
    def inv(self):
        """
        Returns the inverse element
        """
        pass
    
    @abstractmethod
    def __mul__(self, other):
        """
        Retruns the product element
        """
        pass
    
    @abstractmethod
    def __eq__(self, other):
        """
        Returns boolean True if the two elements are equal, False if not.
        Should return TypeError if they can't be compared.
        """
        pass
    
    @abstractmethod
    def Order(self):
        """
        Returns the order of the element. 0 indicates infinite.
        """
        pass

class mset(set):
    """
    Basically a set object, but supports element-wise multiplication:
    {1, 2, 3}*a = {1*a, 2*a, 3*a}
    
    Implemented by adding __mul__ and __rmul__
    """
    def __mul__(self, other):
        """
        {1, 2, 3}*x = {1*x, 2*x, 3*x}
        
        If x is a set, 1*x|2*x|3*x
        """
        if isinstance(other, (set, frozenset)):
            result = mset(el_self*el_other for el_self in self for el_other in other)
        else:
            result = mset(element*other for element in self)
        
        return result
    
    def __rmul__(self,other):
        """
        x*{1, 2, 3} = {X*1, x*2, x*3}
        
        If x is a set, x*1|x*2|x*3
        """
        if isinstance(other, (set, frozenset)):
            result = mset(el_other*el_self for el_self in self for el_other in other)
        else:
            result = mset(other*element for element in self)
        
        return result
    
    def __str__(self):
        return '{'+', '.join(str(element) for element in self) + '}'

class Group:
    """
    The algebraic group.
    """
    
    @classmethod
    def mul(x,y):
        return x*y

    def __init__(self, generators, bin_op = None):
        """
        The group is initialized with any number of elelments as generators.
        The elements are the generators of the group.
        
        bin_op is the binary operation of the group.  If it is none,
        it is assumed the elements implement multiplication.
        """
        
        # There is no way to see if the group is giong to be finite
        # but maybe we should check that they are all finite
        
        if bin_op is None:
            bin_op = Group.mul
            
        self.bin_op = bin_op
        self.generators = mset(generators)
        self._elements = None
        self._center = None
    
    @property
    def elements(self):
        """
        the elements of the group
        """
        
        if self._elements is None:
            self._elements = mset(self.generators)
            
            num_elements = len(self._elements)
            new_elements = 1
            # while we don't necesarily have all elements
            while new_elements:
                
                # generate all products. Not guarenteed to finish :) !
                for a,b in itertools.product(self._elements, self._elements):
                    self._elements.add(self.bin_op(a,b))
                    
                new_elements = len(self._elements) - num_elements
                num_elements = len(self._elements)
                
        return self._elements
            
    
    @property
    def center(self):
        """
        returns the center of the group (all comuting elements)
        """
        if self._center is None:
            self._center = mset()
            for a in self.elements:
                if all(self.bin_op(a,b) == self.bin_op(b,a) for b in self.elements):
                    self.center.add(a)
        return self._center
    
    def __eq__(self, other):
        """
        Do the groups have the same elements.
        """
        if self.bin_op is None:
            return self.elements == other.elements
        else:
            return self.elements == other.elements and self.bin_op == other.bin_op
    
            
        
        
        
        

from abc import ABCMeta, abstractmethod

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

class group:
    pass

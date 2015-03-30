from abc import ABCMeta, abstractmethod
import itertools
import collections

def gcd_2(m,n):
	if n==0:
		return m
	r = m%n
	return(abs(gcd(n,r)))

def gcd(*args):
    return reduce(gcd_2, args)

def sign(n):
    if n==0:
        return 0
    else:
        return abs(n)/n

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
        return
    
    @abstractmethod
    def __mul__(self, other):
        """
        Returns the product of the two elements
        """
        return
    
    def __pow__(self, n):
        """computes the power of the element using the fast exponentiation method
        n: integer"""
        
        if (type(n) != int and type(n) != long) or (n<0):
            raise TypeError(str.format("Can't raise element to {}.\n Must be non-negative integer.",n))
        
        bin_pow = format(n,'b')[::-1]
        prod = self.identity() # start with the identity
        square = prod
        mask = 1
        while mask <= n:
            bit = n & mask
            if square == self.identity():
                square = self
            else:
                square = square * square
            if bit != 0:
                prod = prod * square
            mask <<= 1
        return prod    
    

    @abstractmethod
    def __eq__(self, other):
        """
        Returns boolean True if the two elements are equal, False if not.
        Should return TypeError if they can't be compared.
        """
        return
    
    @abstractmethod
    def __hash__(self, other):
        """
        should hash itself based on value, so that of a == b, then
        a.__hash__() == b.__hash__()
        """
        return
    
    @classmethod
    @abstractmethod
    def identity(cls):
        """
        returns the identity element
        """
        return

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


class Group(object):
    """
    The algebraic group.
    """
    
    @classmethod
    def mul(cls,x,y):
        return x*y

    def __init__(self, generators, bin_op = None):
        """
        The group is initialized with any number of elelments as generators.
        The elements are the generators of the group.
        
        bin_op is the binary operation of the group.  If it is none,
        it is assumed the elements implement multiplication.
        """
        
        if bin_op is None:
            bin_op = Group.mul
            
        self.bin_op = bin_op
        self.generators = mset(generators)
        self._elements = None
        self._center = None
        
    def __eq__(self, other):
        """
        Do the groups have the same elements and the same operation
        """
        return self.elements == other.elements and self.bin_op == other.bin_op
    
    def __str__(self):
        return self.elements.__str__()
    
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
        returns the center of the group (all commuting elements)
        """
        if self._center is None:
            self._center = mset()
            for a in self.elements:
                if all(self.bin_op(a,b) == self.bin_op(b,a) for b in self.elements):
                    self.center.add(a)
        return self._center   
    
    def __mod__(self, other):
        """
        Used for creating left cosets, just invokes division.
        """
        
        return self.__div__(other)
    
    def __div__(self, other):
        """
        Creates left cosets. If other is normal in G, returns a group.
        """
        
        return NotImplemented


class SGroup(Group):
    """
    A symmetric group object
    """
    
    def __init__(self, n):
        """
        Takes the number of elements to be permuted
        """

        if not(isinstance(n, int) and n > 0):
            raise TypeError(str.format("Cant create symmetric group on {} elements.\n Argument must be positive integer", n))

        self.n = n
        super(SGroup, self).__init__([Perm(tup) for tup in itertools.combinations(range(1,n+1), 2)])
    
    @property
    def elements(self):
        if self._elements is None:
            perms = itertools.permutations(range(self.n))
            self._elements = mset(Perm(list(perm), validate = False) for perm in perms)

        return self._elements


class Perm(Element):
    """
    A permutation
    """
    
    @classmethod
    def identity(cls):
        """
        returns the identity permutation
        """
        
        return Perm([])
    
    @classmethod
    def validate_list(cls, l):
        """
        Returns boolean.  Could this list represent a permutation?
        """
        length = len(l)
        max_so_far = 0
        zero_in = False
        one_in = False
        for el in l:
            
            # only accept ints
            if type(el) != int:
                return False
            
            # update max value
            if el > max_so_far:
                max_so_far = el
            
            # see if 0 or 1 is in the lists
            zero_in |= el == 0
            one_in |= el == 1              
        
        # see that no elements are repeated
        if len(set(l)) != length:
            return False
        
        # see that it contains a 1 or a 0
        if not(zero_in) and not(one_in) and length>0:
            return False
        
        # see that we skip no numbers
        if length > 0:
            if max_so_far != length - int(zero_in):
                return False
        
        return True

    @classmethod
    def format_list(cls, l):
        """
        Standerdizes a list that represents a permutaiton.
        Shortens, make it index from 0
        """
        # non-destructive
        l = list(l)

        # make the list start with 0
        if not(0 in l):
            l = [el - 1 for el in l]
        
        # remove useless end peices
        for el in reversed(l):
            if el == l.index(el):
                l.remove(el)
            else:
                break
        
        # make empty lists become [0]
        if len(l) == 0:
            return [0]
        
        return l
    
    @classmethod
    def make_cycles(cls, l):
        """
        Given a list, returns the cycle representation of the permutation.
        
        Assumes the list is in standardized representation.
        """
        
        unpermuted = range(len(l))
        permuted = list(l)
        
        cycles = ()
        cycle = ()
        while unpermuted:
            if len(cycle) == 0:
                # choose the lowest number we haven't used to start
                cycle += (unpermuted[0] + 1,)
            
            else:
                next = permuted[cycle[-1] - 1] + 1
                
                if next != cycle[0]:
                    # if we haven't looped around yet 
                    cycle += (next,)
                
                else:
                    # we are finished with this cycle
                    cycles += (cycle,)
                    
                    # remove the numbers we have used
                    for num in cycle:
                        unpermuted.remove(num - 1)
                    
                    # reset for the next cycle
                    cycle = ()
        
        # remove singletons if there is more than one cycle total
        if len(cycles) > 1:
            trimmed = ()
            for cycle in cycles:
                if len(cycle) > 1:
                    trimmed += (cycle,)
            
            cycles = trimmed

        return cycles
    
    @classmethod
    def make_list(cls, cycles):
        """
        Returns permuted list from the tuple of cycles
        """
        
        # get the largest element in any of the cycles
        max_el = max([max(cycle) for cycle in cycles])
        permuted_list = range(max_el)
        
        # apply each cycle
        for cycle in cycles:
            # note: we dont have to iterate through them reversed because
            # applying the permutations positionally in one order is the same as
            # applying them based on value in the other order.
            
            unpermed_list = list(permuted_list)
            for i in range(len(cycle)):
                permuted_list[cycle[i] - 1] = unpermed_list[cycle[(i + 1) % len(cycle)] - 1]
        
        return Perm.format_list(permuted_list)

    @classmethod
    def validate_cycle(cls, cycle):
        """
        Returns boolean. Is tuple a valid cycle?
        """

        # can only contain integers
        if any([type(el)!= int for el in cycle]):
            return False
        
        # look for repeats
        if any([el in cycle[cycle.index(el)+1:] for el in cycle]):
            return False
        
        # look for non-positive
        if any([el < 1 for el in cycle]):
            return False
        
        return True
    
    def __init__(self, perm, validate = True):
        """
        Takes in a permutation, either as a permuted list or a tuple of cycles
        
        perm: the permutation that this Perm object represents.
            
            Valid formats:
            * a list from 0 to n that has been permuted by the permutation you want this objec to represent.  e.g. [0,1,3,2] represents the permutatio nthat switched the 3rd and fourth element.
            * the cycle representation. one tuple represents a cycle.  To have multiple cycles, each should be a term in a tuple.   e.g. ((1,2),(3,4)).
            
        validate: boolean.  If `validate` is True, the input will be checked to make sure it validly represents a permutation.  This is the default.  If False, no validation will occure.  This is faster.
        """
        self._list = None
        self._cycles = None
        
        if type(perm) == list:
            # treate input as a numeric list that has been permuted
            
            # validate the list format
            if not(validate):
                self._list  = self.format_list(perm)
            
            elif self.validate_list(perm):
                self._list  = self.format_list(perm)
                
            else:
                raise TypeError("Improperly formatted list input: " + str(perm))
        
        elif type(perm) == tuple:
            # treate input as tuple of cycles
            
            # if it is a tuple of integers, turn into a singleton
            if len(perm) > 0:
                if type(perm[0]) == int:
                    perm = (perm,)
            else:
                # interpret empty tuple as identity
                perm = ((1,),)
            
            # validate cycle format
            if not(all(self.validate_cycle(cycle) for cycle in perm)):
                raise TypeError("Improperly formatted cycle input: " + str(perm))
            
            # the following order simplifies the cycles (multiplies them, as it were)
            self._list = Perm.make_list(perm)
            self._cycles = Perm.make_cycles(self._list)
        
        elif type(perm) == type(self):
            # just make a copy
            self._list = list(perm.list)
            self._cycles = perm.cycles
            
        else:
            raise TypeError("Can't create Perm out of type " + str(type(perm)))
            
    
    @property
    def cycles(self):
        if self._cycles is None:
            self._cycles = Perm.make_cycles(self._list)
        
        return self._cycles
    
    @property
    def list(self):
        if self._list is None:
            self._list = Perm.make_list(self._cycles)
        
        return self._list
    
    def __call__(self, iterable):
        """
        Apply the permutation to an iterable object.  Returns type error if
        the object is not iterable or is simply too short.
        """
        # check that the  thing is iterable
        if not(isinstance(iterable, collections.Iterable)):
            raise TypeError("Operand not iterable. Operand:" + str(type(iterable)))
        
        # check the length of the iterable
        if len(iterable) < len(self.list):
            raise TypeError("Can't apply permutation: iterable too short. " + str(iterable))
            
        # copy we will permute and return
        permuted = type(iterable)(iterable)
        
        # apply list permutation to the iterable
        try:
            for i in range(len(self.list)):
                permuted[i] = iterable[self.list[i]]
        
        except TypeError:
            # if the iterable type doesn't support item assignment
            permuted = type(iterable)()
            for i in range(len(self.list)):
                permuted += iterable[self.list[i]:self.list[i]+1]
            
            # add in stuff at the end that wasnt touched by the permutation
            permuted += iterable[i+1:]
        
        return permuted
    
    def __eq__(self, other):
        """
        if the list is the same, they have to be the same
        """
        
        try:
            return self.list == Perm(other).list
        except TypeError as e:
            raise TypeError(str(e) + "\nCan't compare equality of Perm with type "+ str(type(other)))
    
    def __mul__(self, other):
        """
        multiplying permutations is just concatenating their cycles :)
        """
        try:
            return(Perm(self.cycles + Perm(other).cycles))
        except TypeError:
            return NotImplemented
    
    def __hash__(self):
        """
        just use the cycles to hash
        """
        return str(self.list).__hash__()
    
    def __str__(self):
        return ''.join(str(cycle).replace(',', '') for cycle in self.cycles)
    
    def inv(self):
        """
        return the inverse permutation
        """
        
        # simple.  Just reverse all the cycles.
        
        inv_cycles = tuple()
        for cycle in reversed(self.cycles):
            inv_cycles += tuple(reversed(cycle))
        
        return Perm(inv_cycles)
    
    def Order(self):
        """
        Returns the of the permutation. 
        """
        
        lengths = [len(cycle) for cycle in self.cycles]
        return lcm(*lengths)        
        

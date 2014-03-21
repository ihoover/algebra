import collections
import itertools

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
            result = mset()
            for element in other:
                #result = result | self*element
                result |= self*element
        
        else:
            result = mset([element*other for element in self])
        
        return result
    
    def __rmul__(self,other):
        """
        x*{1, 2, 3} = {X*1, x*2, x*3}
        
        If x is a set, x*1|x*2|x*3
        """
        if isinstance(other, (set, frozenset)):
            result = mset()
            for element in other:
                result |= element*self
        
        else:
            result = mset([other*element for element in self])
        
        return result
    
    def __str__(self):
        return '{'+', '.join(str(element) for element in self) + '}'


class SGroup(object):
    """
    A symmetric group object
    """
    
    def __init__(self, n):
        """
        Takes the number of elements to be permuted
        """
        
        if not(isinstance(n, int) and n > 1):
            raise TypeError
        
        # base case is n == 2, {(1), (1,2)}
        if n == 2:
            self.elements = mset({Perm(()), Perm((1,2))})
        
        else:
            ## generate all transpositions with the n'th element
            #trans = [Perm((i+1, n)) for i in range(n-1)]

            ## multiply these transpositions by all permutations on n-1
            ## elements to get the new elements of Sn
            #prev = SGroup(n-1)
            #self.elements = prev.elements | prev.elements*set(trans)
            
            # using itertools we get better performance
            perms = itertools.permutations(range(n))
            self.elements = mset(Perm(list(perm)) for perm in perms)
         
    def __str__(self):
        return self.elements.__str__()

class Perm(object):
    """
    A permutation
    """
    
    @classmethod
    def validate_list(cls, l):
        """
        Returns boolean.  Could this list represent a permutation?
        """
        
        # see that all entries are ints
        if any([type(el)!=int for el in l]):
            return False
        
        # see that no elements are repeated
        if len(set(l)) != len(l):
            return False
        
        # see that it contains a 1 or a 0
        if not(0 in l) and not(1 in l) and len(l)>0:
            return False
        
        # see that we skip no numbers
        if len(l) > 0:
            if max(l) != len(l) - int(0 in l):
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
        
        Assumes the list is in internal representation.
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
    
    def __init__(self, perm):
        """
        Takes in a permutation, either as a permuted list or a tuple of cycles
        """
        
        if type(perm) == list:
            # treate input as a numeric list that has been permuted
            
            # validate the list format
            if self.validate_list(perm):
                self.list  = self.format_list(perm)
                # generate the cycle representation
                self.cycles = Perm.make_cycles(self.list)
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
            if not(all([self.validate_cycle(cycle) for cycle in perm])):
                raise TypeError("Improperly formatted cycle input: " + str(perm))
            
            # the following order simplifies the cycles
            self.list = Perm.make_list(perm)
            self.cycles = Perm.make_cycles(self.list)
        
        elif type(perm) == type(self):
            # just make a copy
            self.list = list(perm.list)
            self.cycles = perm.cycles
            
        else:
            raise TypeError("Can't create Perm out of type " + str(type(perm)))
            
    
    def __call__(self, iterable):
        """
        Apply the permutation to an iterable object.  Returns type error if
        the object is not iterable or is simply too short.
        """
        # check that the  thing is iterable
        if not(isinstance(iterable, collections.Iterable)):
            raise TypeError("Operand not iterable. Operand:" + str(operand))
        
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
        multiplying oermutations is just concatenating their cycles :)
        """
        try:
            return(Perm(self.cycles + Perm(other).cycles))
        except TypeError as e:
            return NotImplemented
    
    def __hash__(self):
        """
        just use the cycles to hash
        """
        return self.cycles.__hash__()
    
    def __str__(self):
        return ''.join(str(cycle).replace(',', '') for cycle in self.cycles)
    
    @property
    def inv(self):
        """
        return the inverse permutation
        """
        
        # simple.  Just reverse all the cycles.
        
        inv_cycles = tuple()
        for cycle in reversed(self.cycles):
            inv_cycles += tuple(reversed(cycle))
        
        return Perm(inv_cycles)

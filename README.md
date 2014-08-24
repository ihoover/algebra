algebra
=========
This is a project to implement the basic algebraic structures of groups in python. It is in its nascent stages and the scope and structure of the project will probably change rapidly. Also, yes, this documentation is incomplete :(  But a heck of a lot better than nothing.

The following classes and abstrac classes are defined:
- `Group` -- a group class
- `Element` -- an abstract class for implementing an element class
- `Perm` -- a class representing a permutation
- `SGroup` -- a class representing a symmetric group, a subclass of `Group`

To run the tests, execute the eponymous shell script `test`.
To add a test file, create a file in the tests directory whose name starts with 'test_'.

##Groups##
The `Group` class is initialized with an iterable of generators, and a binary operation.

`g = Group([2,5], (lambda x,y: (x+y)%31))`

If no binary operation is supplied, the group will use multiplication.  This is handy for constom defined element objects that implement `__mul__`.

####Attributes####
The attributes of a group are:
- `g.elements` -- the set of elements of the group
- `g.generators` -- the set the group was generated from
- `g.center` -- the center of the group, also a set.

####methods####
There are currently no methods.

##Elements##
The `Element` abstract class is a framework for implementing an element class.

####Attributes####
There are currently no attributes

####Methods####
The following methods are required.
- `inv(self)` -- return the inverse of the element instance
- `__mul__(self, other)`
- `__eq__(self,other)`
- `__hash__(self)`
- `order(self)` -- returns the order of the element.  0 is infinite.

##Permutations##
The `Perm`  class represents a permutation.  It is initialized with either a tuple or a list, and the distinction is important.  A permutation can also be initialized from another `Perm` object to create a copy.
- Initializing with a list means that the resulting permutation will be the permutation that has been applied to a sorted list of those integers in order to result in the list supplied.  An empty list is interpreted as the identity permutation. To initialize with a list, the list must be of integers, and it must contain a consecutive set of integers, and it must contain 0 or 1. e.g. `[0,3,2,1]` is valid, but `[0,3,1]` is not, since it doesn't contain 2.  

- When initializing with a tuple, the tuple is interpreted as cycle notation for the permutation.  If more than one cycle is necesary, initialize with a tuple of cycles.  e.g. `Perm((1,2,3))` and `Perm(((1,2),(3,4)))`.  Any set of valid cycles work to create a permutation.  If the cycles are not reduced, the permutation created is the product of the cycles. 

    **NOTE** Currently there are way too many parenthesis for using multiple cycles,  so this behavior will likely change in the next commit so that to initialize with multiple cycles, one simply provides each cycle as an argument. 


####Attributes####
- `list` -- the list representation of the permutation.  i.e. the permutation applied to `range(n)` where `n` is the smallest it can be.
- `cycles` -- the cycle representation of the permutation.  It is a tuple of tuples.

####Methods####
- `__call__(self, other)` -- A permutation can be called on an iterable, and it will apply itself to a copy of the iterable.  e.g. 
    
        >>> Perm([2,1])('abc')
        'bac'

##Symmetric Groups##
`SGroup` is a subclass of the `Group` object and uses the `Perm` object to represent the symmetric group on `n` elements.  It is initialized with the number `n`.  It is should behave exactly like a group. **NOTE** since symmetric groups have n! elements, be careful creating them for more than 9, or so, elements.

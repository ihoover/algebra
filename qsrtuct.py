from qform import Qform, ClassGroup, gcd
import itertools

def legendre_symbol(a,p):
    ls = pow(a, (p-1)/2, p)
    if ls > 1:
        ls = -1
    return ls

def genus(f):
    """
    calculates genus (only for -528)
    """
    
    for tup in itertools.product(range(100), repeat = 2):
        if gcd(f(*tup), f.D) == 1:
            a = f(*tup)
            break
    
    return (legendre_symbol(a,3), legendre_symbol(a,11),  pow(-1,(a-1)/2))

groups = [ClassGroup(D) for D in (-500, -540, -576)]

for g in groups:
    print "\n" + "Class Group for D = " + str(g.D)
    print "\n-------------\n"
    print "Element\t\t\tOrder\n"
    for el in g.elements:
        norm = 1
        el2 = el
        while el2*el2 != el2:
            norm += 1
            el2 = el2*el
        
        print el.__repr__(), '\t', norm
    
    print "\n"

print "\n==================================\n"
print "Genera for C(-528)\n"
for el in ClassGroup(-528).elements:
    print el.__repr__(),'\t', genus(el)

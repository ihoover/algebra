from algebra import *
import math


class Coeffs(object):
    pass


class Qform(Element):
    
    @classmethod
    def isReduced(cls, a,b,c):
        """
        returns bool True if ax^2+bxy+cy^2 is reduced.
        
        """
        
        if (abs(b) <= a) and (a <= c):
            if (c == a) or (abs(b) == a):
                if b >= 0:
                    return True
                else:
                    return False
            else:
                return True
       
        else:
            return False
    
    @classmethod
    def rotate(cls, a, b, c):
        """
        x ->  y
        y -> -x
        """
        
        return (c,-b,a)
    
    @classmethod
    def sheer(cls, a, b, c, m=1):
        """
        x -> x+m*y
        y -> y
        """
        
        return (a, 2*a*m + b, c+b*m+a*m*m)
    
    @classmethod
    def reduced(cls, a,b,c):
        """
        return coeificients of reduced form
        """
        
        while not cls.isReduced(a,b,c):
            # find why it is failing
            if (c<a):
                (a,b,c) = cls.rotate(a,b,c)
                continue
            
            if (abs(b) > a):
                
                if (2*a > b):
                    m = -1
                else:
                    m = (b - b%(2*a))/(2*a)
    
                if sign(a*m) == sign(b):
                    m = -m
    
                (a,b,c) = cls.sheer(a,b,c,m)
            
            if (b < 0) and (a == c):
                (a,b,c) = cls.rotate(a,b,c)
                continue
            
            if (b < 0) and (abs(b) == a):
                (a,b,c) = cls.sheer(a,b,c,1)
        
        return (a,b,c)
    
    def __init__(self, a,b,c):
        """
        Create the equiv class of qudratic forms properly equiv to
            a*x^2 + b*xy+c*y^2
        a,b,c: int
        """

        self.coeffs = Qform.reduced(a,b,c)
        self.a = self.coeffs[0];
        self.b = self.coeffs[1];
        self.c = self.coeffs[2];
        
        self.D = self.b**2 - 4*self.a*self.c

    def __mul__(self, other):
        """
        Multiply equivalence classes
        """
        
        if self.D != other.D:
            msg = "Discriminants don't match"
            raise ValueError(msg)
        
        other_coeffs = other.coeffs
        
        counter = 0
        while gcd (self.a, other_coeffs[0], (self.b + other_coeffs[1])/2) !=1:
            
            # un-reduce it until the relation is satisfied
            if counter % 2 == 0:
                other_coeffs = Qform.rotate(*other_coeffs)
            else:
                other_coeffs = Qform.sheer(*other_coeffs, m=(counter+1)/2)
            counter +=1

        # now solve the relation
        # 1) B == b  mod 2a
        # 2) B == b' mod 2a'
        # 3) B^2 == D  mod 4aa'
        #
        # B is unique mod 2aa'
        
        # 2*a*a'
        taap = 2*self.a*other_coeffs[0]

        condition1 = set((2*self.a*x + self.b)%taap for x in range(taap))
        condition2 = set((2*other_coeffs[0]*x + other_coeffs[1])%taap for x in range(taap))
        condition3 = set(x for x in range(taap) if x**2 % (2*taap) == self.D% (2*taap))
        
        all_conditions = condition1 & condition2 & condition3
        if len(all_conditions) != 1:
            print condition1, condition2, condition3
            print self, other
            msg = str.format("No unique solution to congruence.  Solutions: {}", all_conditions)
            raise ValueError(msg)
        
        B = all_conditions.pop()
        
        return Qform(taap/2, B, (B**2 - self.D)/(2*taap))
    
    def __hash__(self):
        return self.coeffs.__hash__()
    
    def __eq__(self,other):
        return self.coeffs == other.coeffs
    
    def __str__(self):
        if self.b<0:
            op1 = '-'
        else:
            op1 = '+'
        if self.c<0:
            op2 = '-'
        else:
            op2 = '+'
        return str.format("{0}x^2 {1} {2}xy {3} {4}y^2", self.a, op1, abs(self.b), op2, abs(self.c))
    
    def __repr__(self):
        return str(self.coeffs)
    
    def identity(self):
        if (self.D % 4) == 1:
            return Qform(1,1,(1-self.D)/4)
        else:
            return Qform(1,0,-self.D/4)
    
    def inv(self):
        if (self.a == self.c) or (abs(self.b) == self.a):
            return self
        else:
            return Qform(self.a, -self.b, self.c)
    
    def __call__(self, x, y):
        """
        evaluate the form on a x,y pair
        """
        
        return self.a*x**2 + self.b*x*y + self.c*y**2


class ClassGroup(Group):
    """
    The group of equivalence classes of quadratic forms of a give descriminent
    The equivalence relation is proper equivalence
    """
    
    @classmethod
    def allReduced(cls, D):
        def cValue(a,b,D):
            """
            calculate c value, return None of c isn't an integer
            """
            
            c = (b**2-D)/(4.0*a)
            
            if int(c)==c:
                return int(c)
                
            else:
                return None
        
        # calculate reduced forms
        forms = []
        
        # step one, calculate upper bound for a
        max_a = int(math.floor(math.sqrt(-D/3.0)))
        
        # loop thru all possibilities
        for a in range(1,max_a+1):
            for b in range(0,a+1):
                c = cValue(a,b,D)
                if not(c is None) and gcd(a,gcd(b,c))==1 and c>=a:
                    forms.append(Qform(a,b,c))
                    if b<a and b!=0 and a!=c:
                        forms.append(Qform(a,-b,c))
        return forms
    
    def __init__(self, D):
        
        # these reduced forms are our elements
        forms = self.allReduced(D)
        self.D = D
        super(ClassGroup, self).__init__(forms)

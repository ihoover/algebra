from algebra import *

class Qform(Element):
    
    @classmethod
    def isReduced(cls, a,b,c):
        """
        returns bool True if ax^2+bxy+cy^2 is reduced.
        
        """
        
        if (abs(b) <= a) and (a <= c):
            if (c == a) or (abs(b) == a):
                if b > 0:
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
    def sheer(cls, a, b, c, m):
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
    
    def __init__(a,b,c):
        """
        Create the equiv class of qudratic forms properly equiv to
            a*x^2 + b*xy+c*y^2
        a,b,c: int
        """
        
        self.reduced_form = reduced(a,b,c)

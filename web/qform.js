/**********************
 * 
 *	Suite of functions for manipulating quadratic Qforms.
 *  f = ax^2 + bxy + cy^2
 **********************/

var Qform = function(a,b,c){
	this.a = a;
	this.b = b;
	this.c = c;
	this.D = b*b - 4*a*c;
	this.rotate = function(){
		a = this.a;
		b = this.b;
		c = this.c;

		this.a = c;
		this.b = -b;
		this.c = a;
	}

	this.sheer = function(m){
		a = this.a;
		b = this.b;
		c = this.c;

		this.a = a;
		this.b = 2*m*a + b;
		this.c = c + b*m + a*m*m;
	}

	this.reduce = function(){
		while(!isReduced(this)){
			/* find why it isn't reduced */
			if (((this.a == this.c) && (this.b < 0)) || (this.c < this.a)){
				this.rotate();
				continue
			}

			if(Math.abs(this.b) > this.a){
				if (2*this.a > this.b){
					m = -1;
				}
				else{
					m = (this.b - mod(this.b,(2*this.a))) / (2*this.a)
				}

				if (sign(this.a * m) == sign(this.b)){
					m = -m;
				}
				this.sheer(m);
				continue
			}

			if ((this.b < 0) && (Math.abs(this.b) == this.a)){
				this.sheer(1);
				continue
			}
		}
	}

	this.reduce();

	this.inv = function(){
		if ((this.a == this.c) || (Math.abs(this.b) == this.a)){
			return this;
		}
		else{
			return new Qform(self.a, -self.b, self.c);
		}
	}

	this.eq = function(other){
		return ((this.a == other.a) && (this.b == other.b) && (this.c == other.c));
	}

	this.toString = function(){
		res = ""
		if (this.a != 1){
			res += this.a.toString();
		}
		res += 'x^2';

		if (this.b != 0){
			if(this.b < 0){
				b_str = "-";
			}
			else{
				b_str = '+';
			}
			res += b_str;
			if (this.b*this.b !== 1){
				res += Math.abs(this.b).toString();
			}
			res += 'xy';
		}

		res += '+';
		if (this.c != 1){
			res += this.c.toString();
		}
		res += 'y^2';
		return res;
	}
}


function mod(x,y){
	/* needed to fix javascript bug with mod :( */
	return ((x%y)+y)%y
}

function sign(n){
	/*needed because sign is not implemented in IE or Safari*/
	if (n == 0){
		return 0;
	}
	else{
		return n/Math.abs(n);
	}
}

function gcd(m,n){
	if (n==0){
			return Math.abs(m);
	}
	r = mod(m,n);
	return(Math.abs(gcd(n,r)));
}

function isReduced(f){
	/* Returns boolean if quadratic Qform is reduced or not */
	if((Math.abs(f.b) <= f.a) && (f.a <= f.c)){
		if((f.c == f.a) || Math.abs(f.b) == f.a){
			if (f.b >= 0){
				return true;
			}
			else{
				return false;
			}
		}
		else{
			return true;
		}
	}
	else{
		return false;
	}

}

function rotate(f){
	/*
	x ->  y
	y -> -x
	*/
	
	return new Qform(f.c, -f.b, f.a);
}

function sheer(f, m){
	/*
	x -> x + my
	y -> y
	*/

	return new Qform(f.a, 2*m*f.a + f.b, f.c + f.b*m + f.a*m*m);
}

function reduce(f){
	/* Reduce the quadratic Qform */
	while(!isReduced(f)){
		/* find why it isn't reduced */
		/*if(f.c < f.a){
			f = rotate(f);
			continue;
		}*/

		if (((f.a == f.c) && (f.b < 0)) || (f.c < f.a)){
			f = rotate(f);
			continue
		}

		if(Math.abs(f.b) > f.a){
			if (2*f.a > f.b){
				m = -1;
			}
			else{
				m = (f.b - mod(f.b,(2*f.a))) / (2*f.a)
			}

			if (sign(f.a * m) == sign(f.b)){
				m = -m;
			}
			f = sheer(f,m);
			continue
		}

		if ((f.b < 0) && (Math.abs(f.b) == f.a)){
			f = sheer(f,1);
			continue
		}
	}

	return f
}

function mul(f1, f2){
	/*
	 * Multiply two quadratic equivalence classes
	 */

	if (f1.D != f2.D){
		alert("Attemted to multiply two Qforms of unequal descriminant :(");
		return;
	}


	// play with unreducing the quadratic Qform until the relation is satisfied
	f2 = new Qform(f2.a, f2.b, f2.c);
	counter = 0;
	while ([f1.a, f2.a, (f1.b + f2.b)/2].reduce(gcd) != 1){
		if (mod(counter,2)==0){
			f2.rotate();
			//f2 = rotate(f2);
		}
		else{
			f2.sheer((counter+1)/2);
			//f2 = sheer(f2, (counter+1)/2);
		}
		counter++;
		if (counter>200){
			alert("can't satisfy condition for multiplication :(");
		}
	}

	/*
	 * Now we solve the following conditions:
	 * 
	 * 1) B   == f1.b mod 2*f1.a
	 * 2) B   == f2.b mod 2*f2.a
	 * 3) B^2 == D mod 4*f1.a*f2.a
	 *
	 * B is unique mod 2*f1.a*f2.a
	 */

	B = 0
	while(B <= 2*f1.a*f2.a){
		if ((mod(B, 2*f1.a) == mod(f1.b, 2*f1.a)) &&
			(mod(B, 2*f2.a) == mod(f2.b, 2*f2.a)) &&
			(mod(B*B, 4*f1.a*f2.a) == mod(f1.D, 4*f1.a*f2.a))){

			break;
		}
		B++;
	}

	return new Qform(f1.a*f2.a, B, (B*B - f1.D)/(4*f1.a*f2.a));
}

function identity(D){
	if(mod(D,4) == 1){
		return Qform(1,1,(1-D)/4);
	}
	else{
		return Qform(1,0,-D/4);
	}
}

function allReduced(D){
	cValue = function(a,b,D){
		// calculate c-value
		// returns NaN if c is not an integer

		c = (b*b - D)/(4.0*a);
		if(Math.floor(c) == c){
			return c;
		}
		else{
			return NaN;
		}
	}

	var forms = [];

	// calculate upper bound
	max_a = Math.floor(Math.sqrt(-D/3.0));

	for(a = 1; a <= max_a; a++){
		for(b = 0; b<=a; b++){
			c = cValue(a,b,D);

			// conditions for being reduced
			if(!isNaN(c) && [a,b,c].reduce(gcd) == 1 && c>=a){
				forms.push(new Qform(a,b,c));
				if((b < a) && (b != 0) && (a!=c)){
					forms.push(new Qform(a,-b,c))
				}
			}
		}
	}

	return forms;
}

contains_qform = function(list, qform){
	for(i=0; i<list.length; i++){
		if(qform.eq(list[i])){
			return true;
		}
	}
	return false;
}
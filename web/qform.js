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
			return new Qform(this.a, -this.b, this.c);
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
				b_str = " - ";
			}
			else{
				b_str = ' + ';
			}
			res += b_str;
			if (this.b*this.b !== 1){
				res += Math.abs(this.b).toString();
			}
			res += 'xy';
		}

		res += ' + ';
		if (this.c != 1){
			res += this.c.toString();
		}
		res += 'y^2';
		return res;
	}

	this.toStringHtml = function(){
		return this.toString().replace(/\^2/g, "<sup>2</sup>");
	}

	this.toStringMathJax = function(){
		return "\\(" + this.toString() + "\\)";
	}

	this.toStringCompact = function(){
		return "(" + this.a.toString() + " " + this.b.toString() + " " + this.c.toString()+")";
	}

	this.eval = function(x,y){
		return this.a*x*x + this.b*x*y + this.c*y*y;
	}

	this.character = function(a){
		/* evaluates the assigned character of the quadratic form class...
			It doesn't get much more cryptic than this function.  For a full
			explination see 'Primes of the form x^2+ny^2' by David Cox, Chapter 1,
			section 3 */
		var epsilon = function(a){
			return intPow(-1, (a*a - 1)/8);
		}

		var delta = function(a){
			return intPow(-1, (a-1)/2);
		}

		var characters = []
		var oddPrimes = getOddPrimeFactors(this.D);
		for (var i = 0; i < oddPrimes.length; i++){
			characters.push(function(a){return LegendreSymbol(a, oddPrimes[i]);});
		}

		if(mod(this.D, 4) === 0){
			var n = this.D/-4;
			if((mod(n,4) === 1) || (mod(n,8) === 4)){
				characters.push(delta);
			}
			else if (mod(n,8) === 2) {
				characters.push((function(a){return delta(a)*epsilon(a);}));
			}
			else if (mod(n,8) === 6) {
				characters.push(epsilon);
			}
			else if (mod(n,8) === 0){
				characters.push(delta);
				characters.push(epsilon);	
			}
		}

		var res = [];
		for (var i = 0; i < characters.length; i++){
			res.push(characters[i](a));
		}

		return res;
	}

	this.genus = function(){
		/* returns an array like [-1,1,1,-1] which is unique to the genus for
			the specific discriminant.

			It doesn't get much more cryptic than this function.  For a full
			explination see 'Primes of the form x^2+ny^2' by David Cox, Chapter 1,
			section 3 */

		// find output relatively prime to the ddiscriminant
		var a = 0;
		for(var i = 1; i<100; i++){
			for(var j = 1; j < 100; j++){
				if(gcd(this.eval(i,j), this.D) === 1){
					a = this.eval(i,j);
					break;
				}
			}
			if(a != 0){
				break;
			}
		}

		// if we failed to find an input that gives rel prime output
		if (a===0){
			alert("couldn't find rel prime outpur :(");
			return
		}

		return this.character(a)
	}
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
		return new Qform(1,1,(1-D)/4);
	}
	else{
		return new Qform(1,0,-D/4);
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

function contains_qform(list, qform){
	for(i=0; i<list.length; i++){
		if(qform.eq(list[i])){
			return true;
		}
	}
	return false;
}

function mod(x,y){
	/* needed to fix javascript bug with mod :( */
	if(y==0){
		return x;
	}
	return ((x%y)+y)%y;
}

function sign(n){
	/*needed because Math.sign is not implemented in IE or Safari*/
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

function getOddPrimeFactors(integer){
	var factors = getPrimeFactors(integer);
	if (factors[0] == 2){
		return factors.slice(1);
	}
	else{
		return factors;
	}
}

function getPrimeFactors(integer, factors){
	if(factors===undefined){
		factors = [];
	}
	integer = Math.abs(integer);
	quotient = 0;

	for(var i = 2; i <= Math.sqrt(integer); i++){
		quotient = integer/i;

		if(quotient === Math.floor(quotient)){
			integer = integer/i;
			if (factors.length > 0){
				if(factors[factors.length - 1] !== i){
					factors.push(i);
				}
			}
			else{
				factors.push(i);
			}
			return getPrimeFactors(integer,factors);
		}
	}
	if (factors.length > 0){
		if(factors[factors.length - 1] !== integer){
			factors.push(integer);
		}
	}
	else{
		factors.push(integer);
	}
	return factors;
}

function dec2bin(dec){
    /* binary representation */
    return (dec >>> 0).toString(2);
}

function intPow(base, exponent, modulus){
	if (modulus===undefined){
		modulus = 0;
	}
	var binExp = dec2bin(exponent);
	var res = 1;
	var square = base;
	for (var i = 0; i < binExp.length; i++){
		if (binExp[binExp.length - i - 1] === "1"){
			res = mod(res*square, modulus);
		}
		square = mod(square*square, modulus);
	}
	return res
}

function LegendreSymbol(a,p){
	var res = intPow(a,(p-1)/2,p);
	if (res > 1){
		return -1;
	}
	else{
		return res;
	}
}
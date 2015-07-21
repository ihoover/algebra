QUnit.test( "Test isReduced", function( assert ) {
	assert.equal(isReduced({a:2, b:3, c:4}), false, "b too big" );
	assert.equal(isReduced({a:5, b:3, c:4}), false, "a too big" );
	assert.equal(isReduced({a:5, b:-3, c:5}), false, "b neg" );
	assert.equal(isReduced({a:5, b:0, c:5}), true, "true b zero" );
	assert.equal(isReduced({a:3, b:2, c:5}), true, "true standard" );
	assert.equal(isReduced({a:3, b:2, c:5}), true, "true standard" );
});

QUnit.test("Test helpers", function(assert){
	assert.equal([3,6,9].reduce(gcd), 3, "gcd function multiples of 3");
	assert.equal([10,15,21].reduce(gcd), 1, "gcd rel prime");
	assert.equal(mod(-1,3), 2, "mod functions");
});

QUnit.test("Test getPrimeFactors", function(assert){
	assert.deepEqual(getPrimeFactors(6), [2,3]);
	assert.deepEqual(getPrimeFactors(12), [2,3]);
	assert.deepEqual(getPrimeFactors(13), [13]);
	assert.deepEqual(getPrimeFactors(-6), [2,3]);
	assert.deepEqual(getPrimeFactors(-12), [2,3]);
	assert.deepEqual(getPrimeFactors(-13), [13]);
	assert.deepEqual(getPrimeFactors(27), [3]);
	assert.deepEqual(getPrimeFactors(8), [2]);
});

QUnit.test("Test getOddPrimeFactors", function(assert){
	assert.deepEqual(getOddPrimeFactors(6), [3]);
	assert.deepEqual(getOddPrimeFactors(12), [3]);
	assert.deepEqual(getOddPrimeFactors(13), [13]);
	assert.deepEqual(getOddPrimeFactors(210), [3,5,7]);
	assert.deepEqual(getOddPrimeFactors(8), []);
});

QUnit.test("Test intPow", function(assert){
	assert.deepEqual(intPow(2,0,0), 1);
	assert.deepEqual(intPow(11,0,0), 1);
	assert.deepEqual(intPow(0,11,0), 0);
	assert.deepEqual(intPow(2,3,0), 8);
	assert.deepEqual(intPow(2,3,3), 2);
	assert.deepEqual(intPow(5,4,0), 625);
	assert.deepEqual(intPow(5,32,65537), 33457);
	assert.deepEqual(intPow(-1,4,0), 1);
	assert.deepEqual(intPow(-1,41,0), -1);
});

QUnit.test("test LegendreSymbol", function(assert){
	assert.deepEqual(LegendreSymbol(0,3), 0);
	assert.deepEqual(LegendreSymbol(0,11), 0);
	assert.deepEqual(LegendreSymbol(1,3), 1);
	assert.deepEqual(LegendreSymbol(1,23), 1);
	assert.deepEqual(LegendreSymbol(2,3), -1);
	assert.deepEqual(LegendreSymbol(2,5), -1);
	assert.deepEqual(LegendreSymbol(3,5), -1);
	assert.deepEqual(LegendreSymbol(4,5), 1);
	assert.deepEqual(LegendreSymbol(2,7), 1);
	assert.deepEqual(LegendreSymbol(3,7), -1);
	assert.deepEqual(LegendreSymbol(4,7), 1);
	assert.deepEqual(LegendreSymbol(5,7), -1);
	assert.deepEqual(LegendreSymbol(6,7), -1);
	assert.deepEqual(LegendreSymbol(12345,331), -1);
});

QUnit.test("Test reduce", function(assert){
	var f1 = new Qform(95, -87, 21);
	var f2 = new Qform(1,1,2);
	
	// new object tests
	assert.deepEqual(reduce(f1), new Qform(5,-3,21), "not originally reduced");
	assert.deepEqual(reduce(f2), f2, "already reduced");

	// object methods (modifying) tests
	old_f1 = new Qform(f1.a, f1.b, f1.c);
	f1.reduce();

	old_f2 = new Qform(f2.a, f2.b, f2.c);
	f2.reduce();

	assert.deepEqual(f1, new Qform(5,-3,21), "not originally reduced");
	assert.deepEqual(f2, old_f2, "already reduced");
});

QUnit.test("Test multiplication", function(assert){
	var f1 = new Qform(4,4,17);
	var f2 = new Qform(5,-2,13);

	assert.deepEqual(mul(f1,f2), mul(f2,f1), "Test Abelian");
	assert.deepEqual(mul(f1,f2), new Qform(20,28,13));
});

QUnit.test("Test equality", function(assert){
	var f1 = new Qform(4,4,17);
	var f2 = new Qform(5,-2,13);
	var f3 = new Qform(5,-2,13);

	assert.equal(f1.eq(f2), false, "not the same");
	assert.equal(f2.eq(f3), true, "different objects, same value")
})

QUnit.test("Test contains_qform", function(assert){
	var f1 = new Qform(4,4,17);
	var f2 = new Qform(5,-2,13);
	l = [f1, f2];

	assert.equal(contains_qform(l, f1), true);
	assert.equal(contains_qform(l, f2), true);
});

QUnit.test("Test allReduced D=-20", function(assert){
	D = -20;
	f1 = new Qform(1,0,5);
	f2 = new Qform(2,2,3);

	l = allReduced(D)
	assert.equal(l.length, 2, "should only be two classes");
	assert.equal(contains_qform(l, f1), true, "contains the form");
	assert.equal(contains_qform(l, f2), true, "contains the form");
});

QUnit.test("Test allReduced D=-108", function(assert){
	D = -108;
	f1 = new Qform(1,0,27);
	f2 = new Qform(4,2,7);
	f3 = new Qform(4,-2,7);
	l = allReduced(D);

	assert.equal(l.length, 3, "should only be three classes");
	assert.equal(contains_qform(l, f1), true, "contains the form");
	assert.equal(contains_qform(l, f2), true, "contains the form");
	assert.equal(contains_qform(l, f3), true, "contains the form");
});

QUnit.test("Test identity", function(assert){
	var forms = [];
	var new_form;
	for(var d = 1; d<200; d++){
		forms = allReduced(-4*d);
		for(var i = 0; i<forms.length; i++){
			new_form = mul(forms[i], identity(forms[i].D));
			assert.equal(new_form.eq(forms[i]), true);
		}
		forms = allReduced(-4*d + 1);
		for(var i = 0; i<forms.length; i++){
			new_form = mul(forms[i], identity(forms[i].D));
			assert.equal(new_form.eq(forms[i]), true);
		}
	}
});

QUnit.test("Test inverse", function(assert){
	var forms = [];
	var id_form;
	var new_form;
	for(var d = 1; d<200; d++){
		forms = allReduced(-4*d).concat(allReduced(-4*d + 1));
		for(var i = 0; i<forms.length; i++){
			id_form = identity(forms[i].D)
			new_form = mul(forms[i], forms[i].inv());
			assert.deepEqual(new_form,id_form);
		}
	}
});

QUnit.test("Test eval", function(assert){
	f = new Qform(2,1,3);
	for(var i = 1; i<50; i++){
		for(var j = 1; j < 50; j++){
			assert.deepEqual(f.eval(i,j), (2*i*i + 1*i*j + 3*j*j));
		}
	}
});

QUnit.test("Test Character functions -151", function(assert){
	// D = -151;
	f = new Qform(1,1,38);
	for (var i=0; i<100; i++){
		assert.deepEqual(f.character(i), [LegendreSymbol(i,151)]);		
	}
});

QUnit.test("Test Character functions -15", function(assert){
	// D = -15
	f = new Qform(1,1,4);
	for (var i=0; i<100; i++){
		assert.deepEqual(f.character(i), [LegendreSymbol(i,3), LegendreSymbol(i,5)]);		
	}
});

QUnit.test("Test Character functions -12", function(assert){
	// D = -4 * 3
	f = new Qform(1,0,3);
	for (var i=0; i<100; i++){
		assert.deepEqual(f.character(i), [LegendreSymbol(i,3)]);		
	}
});

QUnit.test("Test Character functions -20", function(assert){
	// D = -4 * 5 , n = 1 mod 4
	f = new Qform(2,2,3);
	for (var i=0; i<100; i++){
		assert.deepEqual(f.character(i), [LegendreSymbol(i,5), intPow(-1, (i-1)/2)]);		
	}
});

QUnit.test("Test Character functions -40", function(assert){
	// D = -4 * 10 , n = 2 mod 8
	f = new Qform(1,0,10);
	for (var i=0; i<100; i++){
		assert.deepEqual(f.character(i), [LegendreSymbol(i,5), intPow(-1, (i-1)/2) * intPow(-1, (i*i-1)/8)]);		
	}
});

QUnit.test("Test Character functions -8", function(assert){
	// D = -4 * 2 , n = 2 mod 8, no odd prime factors
	f = new Qform(1,0,2);
	for (var i=0; i<100; i++){
		assert.deepEqual(f.character(i), [intPow(-1, (i-1)/2) * intPow(-1, (i*i-1)/8)]);		
	}

});

QUnit.test("Test Character functions -24", function(assert){
	// D = -4 * 6 , n = 6 mod 8, no odd prime factors
	f = new Qform(2,0,3);
	for (var i=0; i<100; i++){
		assert.deepEqual(f.character(i), [LegendreSymbol(i,3), intPow(-1, (i*i-1)/8)]);		
	}
});

QUnit.test("Test Character functions -48", function(assert){
	// D = -4 * 12 , n = 4 mod 8, no odd prime factors
	f = new Qform(1,0,12);
	for (var i=0; i<100; i++){
		assert.deepEqual(f.character(i), [LegendreSymbol(i,3), intPow(-1, (i-1)/2)]);		
	}
});

QUnit.test("Test Character functions -64", function(assert){
	// D = -4 * 16 , n = 0 mod 8, no odd prime factors
	f = new Qform(4,4,5);
	for (var i=0; i<100; i++){
		assert.deepEqual(f.character(i), [intPow(-1, (i-1)/2), intPow(-1, (i*i-1)/8)]);		
	}
});

QUnit.test("Test Genus D=-528", function(assert){
	//
	var D = -528;
	var id_form = identity(D)

	assert.deepEqual(id_form.genus(), [1,1,1]);

	var f = new Qform(4,0,33);
	assert.deepEqual(id_form.genus(), f.genus());

	var f = new Qform(3,0,44);
	assert.deepEqual(f.genus(), [-1,1,-1]);
	assert.deepEqual((new Qform(11, 0, 12)).genus(), [-1, 1, -1]);
	assert.deepEqual((new Qform(8, 4, 17)).genus(), [-1, -1, 1]);
	assert.deepEqual((new Qform(8, -4, 17)).genus(), [-1, -1, 1]);
	assert.deepEqual((new Qform(7, -2, 19)).genus(), [1, -1, -1]);
	assert.deepEqual((new Qform(7, 2, 19)).genus(), [1, -1, -1]);
})
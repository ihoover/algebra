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
})

QUnit.test("Test allReduced D=-20", function(assert){
	D = -20;
	f1 = new Qform(1,0,5);
	f2 = new Qform(2,2,3);

	l = allReduced(D)
	assert.equal(l.length, 2, "should only be two classes");
	assert.equal(contains_qform(l, f1), true, "contains the form");
	assert.equal(contains_qform(l, f2), true, "contains the form");
})

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
})
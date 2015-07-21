/*
 * Javascript for running the index.html page
 */
_D_ = NaN;
compute = function(){
	var text = document.getElementById("D");
	if (text.value == ""){
		return;
	}
	D = parseInt(text.value);
	if(D == _D_){
		return;
	}
	else{
		_D_ = D;
	}
	if (!(D<0) || mod(D,4) > 1){
		var msg = document.getElementById("msg");
		msg.style.visibility = "visible";
		var tbl  = document.getElementById('multable');
		tbl.style.visibility = "hidden";
	}
	else{
		var msg = document.getElementById("msg")
		msg.style.visibility = "hidden";
		tableCreate(D);
	}
}

function tableCreate(D){
	var tbl  = document.getElementById('multable');
	tbl.innerHTML="";
	var forms = allReduced(D);
	var text = "";
	var genus_color = {};

	for (var i = 0; i < forms.length; i++){
		//just a place-holder value
		genus_color[forms[i].genus().toString()] = i;
	}

	var num_genera = Object.keys(genus_color).length;
	var genera = Object.keys(genus_color);

	genera.sort();

	// now go through and set the color
	color_key = 0;
	step = Math.floor(360/(num_genera + 1));
	h = 180;
	s = "75%";
	l = "75%";
	for(var i = 1; i <= genera.length; i++){
		genus_color[genera[genera.length - i]] = "hsl(" + (mod(h + color_key*step, 360)) + "," + s + "," + l + ")"
		color_key ++;
	}
	console.log(genus_color)

	var RENDER_THRESHOLD = 5;
	
	function render(form){
		var text = "";
		if (forms.length < RENDER_THRESHOLD){
			text = form.toStringMathJax();
		}
		else{
			text = form.toStringCompact();
		}
		return text;
	}

	var f; // a form
	for(var i = 0; i <= forms.length; i++){
		var tr = tbl.insertRow();
		for(var j = 0; j <= forms.length; j++){
			var td = tr.insertCell();
			if (j==0 && i > 0){
				f = forms[i-1];
				text = f.toStringMathJax();
				td.className = "header";
			}
			else if (i==0 && j > 0){
				f = forms[j-1]
				text = f.toStringMathJax();
				td.className = "header";
			}
			else if (i>0 && j > 0){
				f = mul(forms[j-1],forms[i-1])
				text =  render(f);
			}
			else{
				text = "\\(\\times\\)";
				td.className = "header";
			}
			td.innerHTML = text;

			if(i + j > 0){
				td.style.backgroundColor = genus_color[f.genus()];
			}
		}
	}
	tableVisible();
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}

function tableVisible(){
	var tbl  = document.getElementById('multable');
	tbl.style.visibility = "visible";
}
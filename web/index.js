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
		MathJax.Hub.Queue(["Typeset",MathJax.Hub], tableVisible);
	}
	// newTypeset();
}

function newTypeset(){
	//MathJax.Hub.Typeset()
	MathJax.Hub.Queue(["Typeset",MathJax.Hub], tableVisible);
}

function tableCreate(D){
	var tbl  = document.getElementById('multable');
	tbl.innerHTML="";
	tbl.style.visibility = "hidden";
	var forms = allReduced(D);
	var text = "";
	for(var i = 0; i <= forms.length; i++){
		var tr = tbl.insertRow();
		for(var j = 0; j <= forms.length; j++){
			var td = tr.insertCell();
			if (j==0 && i > 0){
				text = '\\(' + forms[i-1].toString() + '\\)';
				td.className = "header";
			}
			else if (i==0 && j > 0){
				text = '\\(' + forms[j-1].toString() + '\\)';
				td.className = "header";
			}
			else if (i>0 && j > 0){
				text = '\\(' + mul(forms[j-1],forms[i-1]).toString() + '\\)';
			}
			else{
				text = "\\(\\times\\)";
				td.className = "header";
			}
			td.appendChild(document.createTextNode(text));
		}
	}
}

function tableVisible(){
	var tbl  = document.getElementById('multable');
	tbl.style.visibility = "visible";
}
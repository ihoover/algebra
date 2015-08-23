/*
 * Javascript for running the index.html page
 */
OLD_D = NaN;

ERROR_MSG = "\\(D\\) must be negative and \\(D\\equiv 0,1\\mod 4\\)";
COMP_MSG = "Computing...";
TOO_BIG_MSG = "The discriminant you have entered is very large so the computation might take a while.\nDo you wish to continue?"
TOO_BIG = -100000;

// for rendering on simplybuilt
var tile = document.getElementsByClassName("tile");
if(tile[0]){
	tile[0].style.width = "100%";
}
var banner = document.getElementsByClassName("github-banner");
if(banner[0]){
	banner[0].style.display = "none";
}

validate = function(){
	var text = document.getElementById("D");
	var button = document.getElementById("compute");
	if (text.value == ""){
		return true;
	}
	D = parseInt(text.value);
	if(D == OLD_D){
		return;
	}
	else{
		OLD_D = D;
	}
	
	if (!(D<0) || mod(D,4) > 1){
		showMsg(ERROR_MSG);
		var tbl  = document.getElementById('multable');
		tbl.style.visibility = "hidden";
		button.disabled = true;
		return true;
	}
	else{
		hideMsg();
		button.disabled = false;
		return false;
	}
}
compute = function(){
	var text = document.getElementById("D");
	if (text.value == ""){
		return;
	}
	D = parseInt(text.value);
	if (!(D<0) || mod(D,4) > 1){
		showMsg(ERROR_MSG);
		var tbl  = document.getElementById('multable');
		tbl.style.visibility = "hidden";
	}
	else{
		if(D<TOO_BIG){
			if(!confirm(TOO_BIG_MSG)){
				return;
			}
		}
		showMsg(COMP_MSG);
		setTimeout(function(){tableCreate(D)},100);
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
	step = Math.floor(360/(num_genera+1));
	h = 180;
	s = "75%";
	l = "75%";
	for(var i = 1; i <= genera.length; i++){
		genus_color[genera[genera.length - i]] = "hsl(" + (mod(h + color_key*step, 360)) + "," + s + "," + l + ")"
		color_key ++;
	}
	
	
	
	var RENDER_THRESHOLD = 6;
	var form_tags = {};
	for (var i=0; i < forms.length; i++){
		form_tags[forms[i].toString()] = "f<sub>" + i + "</sub>";
	}
	function render(form){
		var text = "";
		if (forms.length <= RENDER_THRESHOLD){
			text = form.toStringHtml();
		}
		else{
			text = form_tags[form.toString()];
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
				text = f.toStringHtml();
				if (forms.length > RENDER_THRESHOLD){
					text = form_tags[f.toString()] + ": " + text;	
				}
				td.className = "header";
			}
			else if (i==0 && j > 0){
				f = forms[j-1]
				// text = f.toStringHtml();
				text = render(f);
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
	MathJax.Hub.Queue(["Typeset",MathJax.Hub], hideMsg());
}

function tableVisible(){
	var tbl  = document.getElementById('multable');
	tbl.style.visibility = "visible";
}

function hideMsg(){
	var msg = document.getElementById("msg")
	msg.style.visibility = "hidden";
}

function showMsg(text){
	var msg = document.getElementById("msg")
	msg.innerHTML = text;
	msg.style.visibility = "visible";
	MathJax.Hub.Queue(["Typeset",MathJax.Hub, msg]);
}
function DrawHanger(stage, drawcolor = "#C0C0C0", initialclean = false) {
    cnv = document.getElementById("Canvas1");
    ctx = cnv.getContext("2d");
    if(initialclean)ctx.clearRect(0, 0, cnv.width, cnv.height);
    ctx.lineWidth = 2;
    ctx.beginPath();
	ctx.moveTo(10,180); //base
	if(stage<10)ctx.lineTo(50,180);
	ctx.moveTo(30,180); //pole
	if(stage<9)ctx.lineTo(30,20);
	if(stage<8)ctx.lineTo(80,20); //beam
	if(stage<7)ctx.lineTo(80,40); //rope
	if(stage<6){
	    ctx.moveTo(90, 50);
	    ctx.arc(80, 50, 10, 0, Math.PI * 2, false); // head
	}
	ctx.moveTo(80,60); //torso
	if(stage<5)ctx.lineTo(80,100);
	ctx.moveTo(60,75); // hand1
	if(stage<4)ctx.lineTo(80,65);
	if(stage<3)ctx.lineTo(100,75); //hand2
    ctx.moveTo(65, 135); //leg1
    if(stage<2)ctx.lineTo(80, 100);
    if(stage<1)ctx.lineTo(95, 135); //leg2
    ctx.strokeStyle = drawcolor;
	ctx.stroke();
	//console.log("line added")
}

function updateProgressBar(percentage_left){
    document.getElementById('perc_left').style.width =       percentage_left * 10 + '%';
    document.getElementById('perc_used').style.width = 100 - percentage_left * 10 +'%';
}

function init(){
    DrawHanger(0,'#C0C0C0',true);
    window.addEventListener("beforeunload", function(e) {
        //console.log('used_ltrs="'+document.getElementById('used_ltrs').innerHTML+'"');
        if(document.getElementById('used_ltrs').innerHTML.length == 0)return undefined;
        if(document.getElementById('wrong_attempts').innerHTML == '0')return undefined;
        if(document.getElementById('hint').innerHTML.indexOf('_') == -1)return undefined;
        theWarning = "The game is in progress, and it will be lost if you leave the page. Are you sure you want to leave?"
        e.returnValue = theWarning;
        return theWarning;
    });
}
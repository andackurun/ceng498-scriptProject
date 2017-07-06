var canvas =document.getElementById('myCanvas');
var context=canvas.getContext('2d');

var firstX = 0;
var firstY = 0;
var diffX = 0;
var diffY = 0;
var r;
var tmpData;
var text;
var obj;

var state = {}
state.clicking = 0;
state.canvas = document.getElementById("myCanvas");
state.width = 200;
state.height = 100;
state.firstX = 0;
state.firstY = 0;
state.secondX = 0;
state.secondY = 0;
var operationButton;
var set_delay = 5000, callout = function () {
	ajaxCalls(19)
    setTimeout(callout, set_delay);
};
function clearCanvas()
{
	context.clearRect(0, 0, 800, 600);
}
function ajaxCalls(opType,param1, param2, param3, param4, param5, param6)
{
	resetForm();
	$("#opType").val(opType);
	$("#param1").val(param1);
	$("#param2").val(param2);
	$("#param3").val(param3);
	$("#param4").val(param4);
	$("#param5").val(param5);
	$("#param6").val(param6);
	var formData = $("#sendCommandForm").serialize();
	$.ajax({
		type: "POST",
		datatype: "text/xml",
		url: "./cgi-bin/cgiClient.py",
		data: formData,
		success: onSuccess,
		error: onError,
		beforeSend: function() {
			$.mobile.showPageLoadingMsg(true);
		},
		complete: function() {
			$.mobile.hidePageLoadingMsg();
		}
	});
}
function getMousePos(evt)
{
	var rect = canvas.getBoundingClientRect();
	return [evt.clientX - parseInt(rect.left),evt.clientY - parseInt(rect.top)];
}
function Drawline(firstX, firstY, secondX, secondY)
{
	clearCanvas();
	onSuccess(tmpData);	
	context.beginPath();
	context.moveTo(firstX,firstY);
	context.lineTo(secondX, secondY);
	context.stroke();
}
function Drawline2(firstX, firstY, secondX, secondY)
{
	context.beginPath();
	context.moveTo(firstX,firstY);
	context.lineTo(secondX, secondY);
	context.stroke();
}
function Drawcircle(firstX, firstY,radius) {
	clearCanvas();
	onSuccess(tmpData);
	context.beginPath();
	context.arc(firstX, firstY, radius, 0, 2 * Math.PI, false);
	context.stroke();
}
function Drawcircle2(firstX, firstY,radius) {
	context.beginPath();
	context.arc(firstX, firstY, radius, 0, 2 * Math.PI, false);
	context.stroke();
}
function Drawrectangle(firstX, firstY, width, height) {
	clearCanvas();
	onSuccess(tmpData);
	context.beginPath();
	context.rect(firstX, firstY, width,height);
	context.strokeStyle = 'black';
	context.stroke();
}
function Drawrectangle2(firstX, firstY, width, height) {
	context.beginPath();
	context.rect(firstX, firstY, width,height);
	context.strokeStyle = 'black';
	context.stroke();
}

function WriteText(firstX, firstY, txt, size, font) {
	context.font = size + " " + font;
	context.fillText(txt, firstX, firstY);

}
function Drawtriangle(firstX, firstY, diffY)
{
	clearCanvas();
	onSuccess(tmpData);
	context.beginPath();
	context.moveTo(firstX,firstY);
	context.lineTo(firstX-parseInt(diffY/2), firstY+diffY);
	context.stroke();
	context.beginPath();
	context.moveTo(firstX,firstY);
	context.lineTo(firstX+parseInt(diffY/2), firstY+diffY);
	context.stroke();
	context.beginPath();
	context.moveTo(firstX-parseInt(diffY/2), firstY+diffY);
	context.lineTo(firstX+parseInt(diffY/2), firstY+diffY);
	context.stroke();

}
function Drawtriangle2(firstX, firstY, diffY)
{
	context.beginPath();
	context.moveTo(firstX,firstY);
	context.lineTo(firstX-parseInt(diffY/2), firstY+diffY);
	context.stroke();
	context.beginPath();
	context.moveTo(firstX,firstY);
	context.lineTo(firstX+parseInt(diffY/2), firstY+diffY);
	context.stroke();
	context.beginPath();
	context.moveTo(firstX-parseInt(diffY/2), firstY+diffY);
	context.lineTo(firstX+parseInt(diffY/2), firstY+diffY);
	context.stroke();

}


canvas.onmousedown = function(e) 
{
	state.rect = true;
	mouseXY = getMousePos(e);

	state.firstX = mouseXY[0];
	state.firstY = mouseXY[1];
	
	if(operationButton == 20)
	{
		ajaxCalls(20,mouseXY[0], mouseXY[1]);
	}
	else if(operationButton == 13)
	{
		ajaxCalls(13,mouseXY[0], mouseXY[1]);
	}
	else if(operationButton == 16) {
		state.firstX = mouseXY[0];
		state.firstY = mouseXY[1];
	}
	else if(operationButton == 10) {
		WriteText(mouseXY[0], mouseXY[1], text, "30", "Comic Sans MS");
	}

	
}

canvas.onmousemove = function(e) 
{
	if(operationButton == 2)
	{
		if(state.rect) {
			var mouseXY = getMousePos(e);
			diffX = mouseXY[0]-state.firstX;
			diffY = mouseXY[1]-state.firstY;
		 	Drawrectangle(state.firstX, state.firstY, diffX, diffY);
		 }
	}
	else if(operationButton == 3)
	{
		if(state.rect) {
			var mouseXY = getMousePos(e);
			diffX = mouseXY[0]-state.firstX;
			diffY = mouseXY[1]-state.firstY;
		 	Drawrectangle(state.firstX, state.firstY, diffX, diffX);
		 }
	}
	else if(operationButton == 4)
	{
		if(state.rect) {
			var mouseXY = getMousePos(e);
			diffX = mouseXY[0]-state.firstX;
			diffY = mouseXY[1]-state.firstY;
			r = parseInt(Math.sqrt(Math.pow(diffX,2) + Math.pow(diffY,2)) / 2);
			Drawcircle(state.firstX, state.firstY, r);
		 }
	}
	else if(operationButton == 0)
	{
		if(state.rect) {
			var mouseXY = getMousePos(e);
			Drawline(state.firstX, state.firstY, mouseXY[0], mouseXY[1]);
		 }
	}	
	else if(operationButton == 1)
	{
		if(state.rect) {
			var mouseXY = getMousePos(e);
			diffY = mouseXY[1]-state.firstY;
			Drawtriangle(state.firstX, state.firstY, diffY);
		 }
	}
	else if(operationButton == 16) { //move function
		if(state.rect) {
			var mouseXY = getMousePos(e);
			diffX = mouseXY[0]-state.firstX;
			diffY = mouseXY[1]-state.firstY;
			//Drawrectangle2(obj[0]+diffX, obj[1]+diffY, obj[2], obj[3]);
		}
	}

}

canvas.onmouseup = function(e) 
{
	state.rect = false;
	if(operationButton == 2)
	{
		ajaxCalls(2,state.firstX,state.firstY,diffX,diffY);
	}
	if(operationButton == 3)
	{
		ajaxCalls(3,state.firstX,state.firstY,diffX,diffX);
	}
	else if(operationButton == 4)
	{
		ajaxCalls(4,state.firstX,state.firstY,r);
	}
	else if(operationButton == 0)
	{
		var mouseXY = getMousePos(e);
		ajaxCalls(0,state.firstX,state.firstY,mouseXY[0], mouseXY[1]);
	}
	else if(operationButton == 1)
	{	
		var mouseXY = getMousePos(e);
		ajaxCalls(1,state.firstX,state.firstY,state.firstX-parseInt(diffY/2),state.firstY+diffY,state.firstX+parseInt(diffY/2), state.firstY+diffY);
	}
	else if(operationButton == 14)
	{
		var mouseXY = getMousePos(e);
		scale = $("#scale").val();
		ajaxCalls(14,mouseXY[0], mouseXY[1],scale);
	}
	else if(operationButton == 10)
	{
		var mouseXY = getMousePos(e);
		ajaxCalls(10, mouseXY[0], mouseXY[1]);
		
	}
	else if(operationButton == 16) { // move function
		var mouseXY = getMousePos(e);
		ajaxCalls(16,state.firstX,state.firstY,mouseXY[0],mouseXY[1]);
	}
}
function resetForm()
{
	$('#sendCommandForm')[0].reset();
}
function onSuccess(data)
{
	tmpData = data;
	clearCanvas();
	$(data).find('line').each(function () {
		var operanda = $(this).find('startPos');
		var firstx = $(operanda).find('x').text();
		var firsty = $(operanda).find('y').text();
		var operandb = $(this).find('endPos');
		var secondx = $(operandb).find('x').text();
        var secondy= $(operandb).find('y').text();
        var rect = canvas.getBoundingClientRect();
        firstx = parseInt(firstx);
        secondx = parseInt(secondx);
        firsty = parseInt(firsty);
        secondy = parseInt(secondy);
        Drawline2(firstx, firsty, secondx, secondy);
        
	});
	$(data).find('rectangle').each(function () {
		var operanda = $(this).find('startPos');
		var firstx = $(operanda).find('x').text();
		var firsty = $(operanda).find('y').text();
		var width = $(this).find('width').text();
		var height = $(this).find('height').text();
	    firstx = parseInt(firstx);
	    firsty = parseInt(firsty);
	    width = parseInt(width);
	    height = parseInt(height);
        Drawrectangle2(firstx, firsty, width, height);
	});
	$(data).find('square').each(function () {
		var operanda = $(this).find('startPos');
		var firstx = $(operanda).find('x').text();
		var firsty = $(operanda).find('y').text();
		var width = $(this).find('width').text();
	    firstx = parseInt(firstx);
	    firsty = parseInt(firsty);
	    width = parseInt(width);
        Drawrectangle2(firstx, firsty, width, width);
	});
	$(data).find('circle').each(function () {
		var operanda = $(this).find('startPos');
		var firstx = $(operanda).find('x').text();
		var firsty = $(operanda).find('y').text();
		var radius = $(this).find('radius').text();

	    firstx = parseInt(firstx);
	    firsty = parseInt(firsty);
	    radius = parseInt(radius);
        Drawcircle2(firstx, firsty, radius);
	});
	$(data).find('triangle').each(function () {
		var operanda = $(this).find('pointA');
		var operandb = $(this).find('pointB');
		var operandc = $(this).find('pointC');
		
		var firstx = $(operanda).find('x').text();
		var firsty = $(operanda).find('y').text();
		var secondy = $(operandb).find('y').text();
		firstx = parseInt(firstx);
	    firsty = parseInt(firsty);
		
		var difff = secondy-firsty;
	    difff = parseInt(difff);
		Drawtriangle2(firstx,firsty,difff);
	});
	$(data).find('text').each(function () {
		var operanda = $(this).find('startPos');
		var firstx = $(operanda).find('x').text();
		var firsty = $(operanda).find('y').text();
		var size = $(this).find('size').text();
		var font = $(this).find('font').text();
		var txt = $(this).find('string').text();

	    firstx = parseInt(firstx);
	    firsty = parseInt(firsty);
        WriteText(firstx, firsty, txt, size, font);
	});
	$(data).find('result').each(function () {
		$("#returnVal").text($(this).text());
	});
}

function onError(data,status)
{
	alert("Error");
}
$(document).on("pageinit","#mainPage",function(){
		resetForm();
		callout();
		return false;
});

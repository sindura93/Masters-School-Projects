// Rathna Sindura Chikkam | 1001553518
// pong.js
// initialize variables
var courtBoundingClient = new Object();
var gameSpeed = 10;
var ballStrikes = 0;
var maxScore = 0;
var animateBall = new Object();
var ballWidth = 0;
var ballPositionLeft = 0;
var ballPositionTop = 0;
var paddleHeight = 0;
var gameStarted = 0;
var isTimeOutTick = 0;
var vx = 1;
var vy = 1;


//this function initializes the game on page load
function initialize(){
	var courtDiv = document.getElementById("court");
	courtBoundingClient = courtDiv.getBoundingClientRect();
	ballStrikes = 0;
	// get current ball position 
	var ballElement = document.getElementById("ball");
	ballWidth = ballElement.width;
	ballPositionLeft = ball.offsetLeft;
	ballPositionTop = ball.offsetTop;
	// set ball position randomly
	document.getElementById("ball").style.left = (Math.floor(Math.random() * 400) + 1) + "px";
	document.getElementById("ball").style.top = (Math.floor(Math.random() * 400) + 1) + "px";	
	paddleHeight = document.getElementById("paddle").offsetHeight;
	// set paddle position
	document.getElementById("paddle").style.top = ((courtDiv.style.height - paddleHeight)/2) + "px";	
}

//this function starts game either on start button click or a mouse click anywhere on the court
function startGame(){
	if(gameStarted == 0){
		animateBall = setInterval(fun, gameSpeed);
		gameStarted++;
	}
}

//this function sets the game speed on game mode selection
function setSpeed(i){ 
	if(i == 0){ //slow mode
		gameSpeed = 10;
	} else if(i == 1) { //medium mode
		gameSpeed = 4;
	} else if(i == 2) { //fast mode
		gameSpeed = 0.02;
	}
}

// this function resets the entire game
function resetGame(){
	window.location.reload(true);
	document.getElementById("score").innerHTML = maxScore;
}

// this function moves the paddle up and down following the mouse
function movePaddle(e){
	if((e.clientX > courtBoundingClient.left) && (e.clientX < courtBoundingClient.right) && (e.clientY > courtBoundingClient.top) && (e.clientY < courtBoundingClient.bottom - document.getElementById("paddle").offsetHeight - 4)){
		document.getElementById("paddle").style.top = Math.floor(e.clientY - document.getElementById("court").offsetTop) + "px";		
	}
}

// this function updates the max strike score from the previous game
function updateMaxScore(){
	if(maxScore < ballStrikes){
		maxScore = ballStrikes;
		document.getElementById("score").innerHTML = maxScore;
	}
	document.getElementById("strikes").innerHTML = 0;
}

function fun(){
	// check if ball is near border and is about to hit it
	//console.log("Hello");
	borderCrossed();
	// get ball current position
	var ballElement = document.getElementById("ball");
	ballPositionTop = ballElement.offsetTop;
	ballPositionLeft = ballElement.offsetLeft;
	// get paddle current position
	var paddleElement = document.getElementById("paddle");
	paddlePositionTop = paddleElement.offsetTop;
	paddlePositionLeft = paddleElement.offsetLeft;
	// set ball position
	//console.log(ballPositionLeft)
	//console.log(ballPositionTop)
	document.getElementById("ball").style.left = (ballPositionLeft + vx) + "px";
	document.getElementById("ball").style.top = (ballPositionTop + vy) + "px";
	
	if(ballPositionLeft + ballWidth >= paddlePositionLeft){
		if(ballPositionTop + (ballWidth/2.0) > paddlePositionTop && ballPositionTop < paddlePositionTop + paddleHeight - (ballWidth/2.0)){
			if(isTimeOutTick == 0){
				ballStrikes++;
				document.getElementById("strikes").innerHTML = ballStrikes;
				vx = -vx;
				isTimeOutTick++;
			}
			setTimeout(function(){
				isTimeOutTick = 0;
			}, 1800);
		}else if(ballPositionLeft + ballWidth >= courtBoundingClient.width - 4){
			window.clearInterval(animateBall);
			updateMaxScore();
			initialize();
			gameStarted = 0;
		}
	}
}

function borderCrossed(){
	// get current ball position 
	var ballElement = document.getElementById("ball");
	ballHeight = ballElement.height;
	ballWidth = ballElement.width;
	ballPositionLeft = ball.offsetLeft;
	ballPositionTop = ball.offsetTop;
	// reset ball position
	if((ballPositionLeft <= 0) || (ballPositionLeft >= (courtBoundingClient.width - ballWidth))){
		vx = vx * -1;
	}
	if((ballPositionTop <= 0) || (ballPositionTop  >= (courtBoundingClient.height - ballHeight))){
		vy = vy * -1;
	}
}

window.onload = function() {
	initialize();
}

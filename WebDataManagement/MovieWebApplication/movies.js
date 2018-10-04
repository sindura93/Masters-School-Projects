function initialize(){
	document.getElementById("movieResultsColumn").style.display = "none";
	document.getElementById("movieInfoColumn").style.display = "none";
	document.getElementById("searchResults").style.display = "none";
	document.getElementById("movieDetails").style.display = "none";
	document.getElementById("resultsErrorMsg").style.display = "none";
	document.getElementById("movieInfoErrorMsg").style.display = "none";
}

function sendRequest () {
	var xhrMovieByTitle = new XMLHttpRequest();
	var query = (document.getElementById("form-input").value);
	//console.log(query);
	xhrMovieByTitle.open("GET", "proxy.php?method=/3/search/movie&query=" + query);
	xhrMovieByTitle.setRequestHeader("Accept","application/json");
	xhrMovieByTitle.onreadystatechange = function () {
	   if (this.readyState == 4) {
			var searchmoviejson = JSON.parse(this.responseText);
			if((searchmoviejson != "undefined") && (searchmoviejson.results.length > 0)) {
				document.getElementById("movieResultsColumn").style.display = "block";
				document.getElementById("searchResults").style.display = "block";
				document.getElementById("resultsErrorMsg").style.display = "none";
				var resultsSec = document.getElementById("resultsSection");
				
				//check if resultsSec div is empty, if it is not, empty it
				if(resultsSec.innerHTML == "") {
					console.log("resultsSec div was empty");
				} else {
					resultsSec.innerHTML = "";
					document.getElementById("movieInfoColumn").style.display = "none";
				}
				
				// append header row
				var headerRow = document.createElement("div");
				headerRow.className = "row";
				var titleHeaderDiv  = document.createElement("div");
				titleHeaderDiv.innerHTML = "Movie Title";
				titleHeaderDiv.className = "col-9";
				titleHeaderDiv.style.fontWeight = "bold";
				headerRow.appendChild(titleHeaderDiv);
				var dateHeaderDiv = document.createElement("div");
				dateHeaderDiv.innerHTML = "Release Year";
				dateHeaderDiv.className = "col-3";
				dateHeaderDiv.style.fontWeight = "bold";
				headerRow.appendChild(dateHeaderDiv);
				resultsSec.appendChild(headerRow);
				// append search results
				var items = searchmoviejson.results;
				for(var i = 0; i < items.length; i++) {
					var resultRow = document.createElement("div");
					resultRow.className = "row";
					var movieTitle = document.createElement("div");
					movieTitle.className = "col-9";
					movieId = items[i].id;
					movieTitle.id = movieId;
					var movieanchor = document.createElement("a");
					movieanchor.innerHTML = items[i].title;
					movieanchor.setAttribute("href", "#");
					movieanchor.setAttribute("onclick", "javascript:getMovieById("+movieId+")");
					movieTitle.appendChild(movieanchor);
					resultRow.appendChild(movieTitle);
					var moviedate = document.createElement("div");
					if(items[i].release_date.length > 0){
						moviedate.innerHTML = items[i].release_date.slice(0,4);
					} else{
						moviedate.innerHTML = "Date Unavailable in TMDB.";
						moviedate.style.color="#708090";
					}
					//moviedate.innerHTML = items[i].release_date.slice(0,4);
					moviedate.className = "col-3";
					resultRow.appendChild(moviedate);
					resultsSec.appendChild(resultRow);
				}

			} else {
				var resultsSec = document.getElementById("resultsSection");
				//check if resultsSec div is empty, if it is not, empty it
				if(resultsSec.innerHTML == "") {
					console.log("resultsSec div was empty");
				} else {
					resultsSec.innerHTML = "";
				}
				document.getElementById("movieResultsColumn").style.display = "block";
				document.getElementById("searchResults").style.display = "block";
				document.getElementById("resultsErrorMsg").style.display = "block";
			}
		}
	};
	xhrMovieByTitle.send(null);	
}


function getMovieById(movieId){
	//console.log("Entered getMovieById")
	//console.log(movieId)
	var xhrMovieById = new XMLHttpRequest();
	xhrMovieById.open("GET", "proxy.php?method=/3/movie/" + movieId);
	xhrMovieById.setRequestHeader("Accept","application/json");
	xhrMovieById.onreadystatechange = function () {
	   if (this.readyState == 4) {
			var movieinfojson = JSON.parse(this.responseText);
			if(movieinfojson != "undefined"){
				document.getElementById("movieInfoColumn").style.display = "block";
				document.getElementById("movieDetails").style.display = "block";
				document.getElementById("movieInfoErrorMsg").style.display = "none";
				var movieInfoSec = document.getElementById("movieInfoSection");
				
				//check if movieInfoSec div is empty, if it is not, empty it to update new movie selection details
				if(movieInfoSec.innerHTML == "") {
					console.log("movieInfoSec div was empty");
				} else {
					movieInfoSec.innerHTML = "";
				}
				
				//append movie poster				
				var imageRow = document.createElement("div");
				imageRow.className = "row";
				// check if poster is available
				if(movieinfojson.poster_path != null){
					var imageElement = document.createElement("img");
					var posterUrl = "http://image.tmdb.org/t/p/w185/" + movieinfojson.poster_path;
					imageElement.setAttribute("src", posterUrl);
					imageRow.appendChild(imageElement);
				} else {
					imageRow.innerHTML = "Poster unavailable in TMDB.";
					imageRow.style.color="#708090";
				}
				//var posterUrl = "http://image.tmdb.org/t/p/w185/" + json.poster_path;
				//imageElement.setAttribute("src", posterUrl);
				//imageRow.appendChild(imageElement);
				movieInfoSec.appendChild(imageRow);
				movieInfoSec.appendChild(document.createElement("br"));
				// append movie details
				var movieTitle = document.createElement("div");
				movieTitle.className = "row";
				movieTitle.innerHTML = "Title: " + movieinfojson.title;
				movieInfoSec.appendChild(movieTitle);
				movieInfoSec.appendChild(document.createElement("br"));
				var movieGenre = document.createElement("div");
				movieGenre.className = "row";
				movieGenre.innerHTML = "Genre: ";
				// check if genres are available
				if(movieinfojson.genres.length > 0) {
					for (var i=0; i < movieinfojson.genres.length; i++){
						movieGenre.innerHTML += movieinfojson.genres[i].name + "; ";
					}
				} else{
					movieGenre.innerHTML += "<span style='color: #708090;'> Genres are not available for this movie in TMDB.</span>";
				}				
				movieInfoSec.appendChild(movieGenre);
				movieInfoSec.appendChild(document.createElement("br"));
				var movieSummary = document.createElement("div");
				movieSummary.className = "row";
				// check if movie summary is available
				if(movieinfojson.overview.length > 0) {
					movieSummary.innerHTML = "Summary: " + movieinfojson.overview;
				} else{
					movieSummary.innerHTML = "Summary: " + "<span style='color: #708090;'> Movie Summary is not available for this movie in TMDB.</span>";
				}
				//movieSummary.innerHTML = "Summary: " + json.overview;
				movieInfoSec.appendChild(movieSummary);
				movieInfoSec.appendChild(document.createElement("br"));
				getMovieCreditsById(movieId);
			} else {
				var movieInfoSec = document.getElementById("movieInfoSection");
				//check if movieInfoSec div is empty, if it is not, empty it to update new movie selection details
				if(movieInfoSec.innerHTML == "") {
					console.log("movieInfoSec div was empty");
				} else {
					movieInfoSec.innerHTML = "";
				}
				document.getElementById("movieInfoColumn").style.display = "block";
				document.getElementById("movieDetails").style.display = "block";
				document.getElementById("movieInfoErrorMsg").style.display = "block";
			}
		}
	};
	xhrMovieById.send(null);
}

function getMovieCreditsById(movieId){
	//console.log("Entered getMovieById")
	//console.log(movieId)
	var xhrMovieCreditsById = new XMLHttpRequest();
	xhrMovieCreditsById.open("GET", "proxy.php?method=/3/movie/" + movieId + "/credits");
	xhrMovieCreditsById.setRequestHeader("Accept","application/json");
	xhrMovieCreditsById.onreadystatechange = function () {
		if (this.readyState == 4) {
			var moviecreditinfojson = JSON.parse(this.responseText);
			if(moviecreditinfojson != "undefined"){
				var movieInfoSec = document.getElementById("movieInfoSection");
				// append movie cast credit info
				var castInfo = document.createElement("div");
				castInfo.className = "row";
				castInfo.innerHTML = "Cast: ";
				// check if cast info is present 
				if(moviecreditinfojson.cast.length > 0){
					var looplimit = 0;
					if(moviecreditinfojson.cast.length >=5){
						looplimit = 5;
					} else {
						looplimit = moviecreditinfojson.cast.length;
					}
					for(var i=0; i < looplimit; i++){
						castInfo.innerHTML += moviecreditinfojson.cast[i].name + "; ";
					}
				} else{
					castInfo.innerHTML += "<span style='color: #708090;'> Cast Information is not available for this movie in TMDB.</span>";
				}
				
				movieInfoSec.appendChild(castInfo);
			} else {
				document.getElementById("movieInfoColumn").style.display = "block";
				document.getElementById("movieInfoErrorMsg").style.display = "block";
			}
		}
	};
	xhrMovieCreditsById.send(null);
}

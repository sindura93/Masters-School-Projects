var giveninitialLatLng;
var googleMapElement;
var markers=[];
var marker;
var locationarray = [];
var googleMapLatitude;
var googleMapLongitude;

function initialize () {
	giveninitialLatLng = {lat: 32.75, lng: -97.13};
	googleMapLatitude = giveninitialLatLng.lat;
	googleMapLongitude = giveninitialLatLng.lng;
	googleMapElement = new google.maps.Map(document.getElementById('googleMap'), {
		zoom: 16,
		center: giveninitialLatLng
	});

	google.maps.event.addListener(googleMapElement, "click", function (e) {
		googleMapLatitude = e.latLng.lat();
		googleMapLongitude = e.latLng.lng();
		//console.log(googleMapLatitude);
		//console.log(googleMapLongitude);
	});
	
	//verify if bounds changed
	google.maps.event.addListener(googleMapElement, 'bounds_changed', function() {
		center = googleMapElement.getBounds();
        googleMapLatitude = (center.f.b + center.f.f) / 2;
        googleMapLongitude = (center.b.f + center.b.b) / 2;
		//console.log(googleMapLatitude);
		//console.log(googleMapLongitude);
    });
}

function plotGoogleMap(locationarray){
	currentlatlng = {lat: googleMapLatitude, lng: googleMapLongitude}
	googleMapElement.setCenter(currentlatlng);
	if(markers != null && markers != undefined){
		for (i = 0; i < markers.length; i++) {
			markers[i].setMap(null);		
		}
	}
	for (i = 0; i < locationarray.length; i++) {
		marker = new google.maps.Marker({
			position: new google.maps.LatLng(locationarray[i][1], locationarray[i][2]),
			map: googleMapElement,
			title: String(locationarray[i][0]),
			label: String(locationarray[i][0])
		});
		markers.push(marker);
	}
	marker.setMap(googleMapElement);
}

function displaySearchResult (jsonresults) {
	var resultslen = jsonresults.businesses.length;
	var outputelement = document.getElementById("output");
	if(outputelement.innerHTML == "") {
		console.log("outputelement div was empty");
	} else {
		outputelement.innerHTML = "";
	}	
	for(var i=0; i< resultslen; i++){
		//create new row each time
		var rowElement = document.createElement("div");
		rowElement.setAttribute("class","row");
		outputelement.appendChild(rowElement)
		// display image
		var colImgElement = document.createElement("div");
		colImgElement.setAttribute("class","col-4");
		rowElement.appendChild(colImgElement);
		var imageElement = document.createElement("img");
		imageElement.setAttribute("src", jsonresults.businesses[i].image_url);
		imageElement.setAttribute("width","180px");
		colImgElement.appendChild(imageElement);
		// add a space column
		var spacecol = document.createElement("div");
		spacecol.setAttribute("class","col-1");
		rowElement.appendChild(spacecol);
		// display data
		var colDataElement = document.createElement("div");
		colDataElement.setAttribute("class","col-4");
		rowElement.appendChild(colDataElement);
		var titleElement = document.createElement("a");
		titleElement.innerHTML = jsonresults.businesses[i].name;
		titleElement.setAttribute("href", jsonresults.businesses[i].url);
		colDataElement.appendChild(titleElement);
		colDataElement.appendChild(document.createElement("br"));
		var ratingElement = document.createElement("p");
		ratingElement.innerHTML = "Rating: " + jsonresults.businesses[i].rating;
		colDataElement.appendChild(ratingElement);
		// create location marker array
		var locationdetails = [i+1, jsonresults.businesses[i].coordinates.latitude, jsonresults.businesses[i].coordinates.longitude];
		locationarray[i] = locationdetails;		
	}
	plotGoogleMap(locationarray);
}

function sendRequest () {
	var xhr = new XMLHttpRequest();
	var searchterm = (document.getElementById("search").value);
	locationarray = [];
	//var proxyTerm = "proxy.php?term="+searchterm+"&location=Arlington+Texas"+"&limit=10";
	var proxyTerm = "proxy.php?term="+searchterm+"&latitude=" + googleMapLatitude + "&longitude=" + googleMapLongitude + "&limit=10&sort_by=rating";
	//console.log(proxyTerm);
	xhr.open("GET", proxyTerm);
	xhr.setRequestHeader("Accept","application/json");
	xhr.onreadystatechange = function () {
		if (this.readyState == 4) {
			var json = JSON.parse(this.responseText);
			//var str = JSON.stringify(json,undefined,2);
			if((json != "undefined") && (json.businesses.length > 0)) {
				displaySearchResult(json);
			} else {
				document.getElementById("output").innerHTML = "No results found from Yelp. Please try a different search.";
			}			
       }
	};
	xhr.send(null);
}

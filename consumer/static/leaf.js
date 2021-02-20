var mymap = L.map('mapid').setView([51.505, -0.09], 1);
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'access_token'
}).addTo(mymap);


var source = new EventSource("/topic/twitterstream");

source.addEventListener('message', function(e) {
    var data = JSON.parse(e.data);
    latitude = data.place.bounding_box.coordinates[0][0][1];
    longitude = data.place.bounding_box.coordinates[0][0][0];
    username= data.user.name;
    tweet= data.text
    marker = L.marker([latitude,longitude]).addTo(mymap)
            .bindPopup(
                "Username: <strong>"+ username + "</strong> <br> Tweet: <strong>"+tweet +"</strong>"
            )
}, false);

source.addEventListener('open', function(e) {
    console.log("IN OPEN",e);
}, false);
  
source.addEventListener('error', function(e) {
console.log("IN ERROR",e);
}, false);
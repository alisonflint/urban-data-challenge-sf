  function loadMap() {
    var latlng = new google.maps.LatLng(37.780755,-122.419281); 
    var myOptions = {
      zoom: 13,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.TERRAIN
    };
    var map = new google.maps.Map(document.getElementById("map_container"),myOptions);
	
	var styles = [
  {
    stylers: [
      { hue: "#00ffe6" },
      { saturation: -20 }
    ]
  },{
    featureType: "water",
    elementType: "geometry.fill",
    stylers: [
      { saturation: 100 },
	  { "hue": "#c300ff" }
    ]
  },{
    featureType: "road",
    elementType: "labels",
    stylers: [
      { visibility: "off" }
    ]
  }
];

map.setOptions({styles: styles});
  
	// Create a script tag and set the USGS URL as the source.
	var script = document.createElement('script');
	script.src = 'http://sf-data.s3.amazonaws.com/realtime-arrivals.excerpt.json';
	var s = document.getElementsByTagName('script')[0];
	s.parentNode.insertBefore(script, s);

	// Loop through the results array and place a marker for each
    // set of coordinates.
    window.eqfeed_callback = function(results) {	
			for (var i = 0; i < results.features.length; i++) {
			var bus = results.features[i];
			var lat = results.features[i].LATITUDE;
			var lng = results.features[i].LONGITUDE;
			var latLng = new google.maps.LatLng(lat,lng);
			var marker = new google.maps.Marker({
				position: latLng,
				map: map,
				title: bus.PUBLIC_ROUTE_NAME,	
          });
        }
	}
  }

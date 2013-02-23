function loadMap(json) {
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

  var lines = {}
  for (var i = 0; i < json.length; ++i) {
    var bus = json[i].PUBLIC_ROUTE_NAME;
    var spots;
    if (!(bus in lines))
      lines[bus] = [];

    var lat = json[i].LATITUDE;
    var lng = json[i].LONGITUDE;
    spots.append(new google.maps.LatLng(lat, lng));
  }

  for (var line_id in lines) {
    var flightPath = new google.maps.Polyline({
        path: lines[line_id],
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
  }
}

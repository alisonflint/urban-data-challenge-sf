// The actual map.
var map;
// A scale for creating route colors.
var routeColor = d3.scale.category20c();
// A scale for creating colors for each stop based on distance.
var stopColor = d3.scale.quantize()
  .domain([0, 3600])
  .range(colorbrewer.YlOrRd[9]);
// A map from stop identifiers to markers.
var markerMap;
// A map from each tile identifier to all markers in that tile.
var tileMap;
// A list of all currently displayed markers.  Everytime a user clicks on a new
// marker, these nodes are removed from the map and the list is repopulated.
// While in this list, said markers will not be removed when the user moves
// between tiles.
var displayList = [];
// The bin size for breaking down the for displaying only a subset of stops near
// the user's mouse.
var tileBinSize = 100;
var businessMap = {};
var traveltimeChart;

var vis;
var stopGraph;

function setupCharts() {
  traveltimeChart = dc.barChart("#traveltime");

  vis = d3.select("#transit_graph")
    .append("svg:svg")
    .attr('w', 1000)
    .attr('h', 1000);

  stopGraph = d3.layout.force()
      .size([1000, 1000])
      .charge(-1);
}

function loadTransitGraph(transit_graph) {
  console.log(transit_graph);
  stopGraph.nodes(transit_graph.nodes)
    .links(transit_graph.links)
    .start();
  
  var link = vis.selectAll(".link")
    .data(transit_graph.links)
    .enter()
    .append("line")
    .attr("class", "link");

  var node = vis.selectAll('.node')
    .data(transit_graph.nodes)
    .enter()
    .append('circle')
    .attr('class', 'node')
    .attr('r', 5)
    .call(stopGraph.drag);

  node.append("title")
    .text(function(d) { return d.name; });

  stopGraph.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
  });
}

function loadMap() {
  var latlng = new google.maps.LatLng(37.780755,-122.419281); 
  var myOptions = {
    zoom: 13,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  };
  map = new google.maps.Map(document.getElementById("map_container"),myOptions);
  routeColor = d3.scale.category20c();

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
}

var loadBusinesses = function(businessJson) {
  businessMap = businessJson;
};

/**
 * Load the route information.  This is often disconnected from the actual
 * stops but gives a good grounding.
 */
var loadRoutes = function(routeJson) {
  for (var i = 0; i < routeJson.features.length; ++i) {
    var line = routeJson.features[i];
    console.log("plotting route: " + line.properties.LINEABBR);
    for (var c = 0; c < line.geometry.coordinates.length; ++c) {
      var routeStops = line.geometry.coordinates[c];
      var stopPositions = []
      for (var j = 0; j < routeStops.length; ++j)
        stopPositions.push(new google.maps.LatLng(
            routeStops[j][1], routeStops[j][0]));

      var busRoute = new google.maps.Polyline({
          path: stopPositions,
          strokeColor: routeColor(1), //line.properties.LINEABBR),
          strokeOpacity: 1.0,
          strokeWeight: 3
      });
      busRoute.setMap(map);
    }
  }
  console.log("plotted: " + routeJson.features.length);
};

/*
 * Load the stops and store them all according to their stop id.  Also store
 * them based on a truncation of their geo location.
 */
var loadStops = function(stopJson) {
  markerMap = {};
  tileMap = {};
  for (var i = 0; i < stopJson.features.length; ++i) {
    // Get the raw information about the stop.
    var stop = stopJson.features[i];
    var latitutude = parseFloat(stop.properties.LATITUDE, 10);
    var longitude = parseFloat(stop.properties.LONGITUDE, 10);
    var stopid = parseInt(stop.properties.STOPID, 10);

    // Create a new marker for the stop.
    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(latitutude, longitude),
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 4,
        strokeColor: "green"
      },
      stopid: stopid,
      is_displayed: false,
    });
    markerMap[stopid] = marker;

    // Decide which tile this marker falls into.  Everytime the user hovers over
    // a particular tile, bring up all markers within that tile and any nearby
    // tiles.
    var tile_key = getTileKey(latitutude, longitude);
    if (!(tile_key in tileMap))
      tileMap[tile_key] = {"key": tile_key, "markers": []}
    tileMap[tile_key].markers.push(marker);

    // Add an on click listener that's always active.
    google.maps.event.addListener(marker, "click", handleStopClick);
  }

  // For each tile, create an invisible overlap that has a hover listener.
  for (tile_key in tileMap) {
    var key = tileMap[tile_key].key;
    var bounds = new google.maps.LatLngBounds(
      new google.maps.LatLng(convertTileIndex(key[0]-1),
                             convertTileIndex(key[1]-1)),
      new google.maps.LatLng(convertTileIndex(key[0]),
                             convertTileIndex(key[1])));
    var tile = new google.maps.Rectangle();
    tile.setOptions({
      strokeOpacity: 0.0,
      fillOpacity: 0.0,
      map: map,
      bounds: bounds,
      tile_markers: tileMap[tile_key].markers,
    });
    google.maps.event.addListener(tile, "mouseover", mouseHover);
    google.maps.event.addListener(tile, "mouseout", mouseExit);
  }
};

/**
 * Turns a field in an index key into a latitude/longitude value.
 */
var convertTileIndex = function(index) {
  return index / tileBinSize;
};

/** 
 * Removes markers from the map that are not currently being permanently
 * displayed based on which tile the user is hovering over.
 */
var mouseExit = function() {
  var tile_markers = this.tile_markers;
  for (var i = 0; i < tile_markers.length; ++i) {
    var marker = tile_markers[i];
    if (!marker.is_displayed)
      marker.setMap(null);
  }
};

/**
 * Populates the map with new markers that are not currently being permanently
 * displayed based on which tile the user is hovering over.
 */
var mouseHover = function() {
  var tile_markers = this.tile_markers;
  for (var i = 0; i < tile_markers.length; ++i) {
    var marker = tile_markers[i];
    if (!marker.is_displayed)
      marker.setMap(map);
  }
};

/**
 * Makes an ajax request to the server for the distance information from this
 * stop to all reachable stops.  When the ajax call returns, it will permanently
 * highlight the reachable stops with colors based on how far away they are.
 * This also clears the display list and repopulates it.
 */
var handleStopClick = function() {
  // Clear all currently permanently displayed markers.
  for (var i = 0; i < displayList.length; ++i) {
    var marker = displayList[i];
    marker.setMap(null);
    marker.is_displayed = false;
    marker.icon.strokeColor = 'green';
  }

  console.log(d3.select("#controls #start_time").value);

  // Mark the clicked marker as displayed.
  displayList = [this];
  this.is_displayed = true;

  console.log("requesting: " + this.stopid);

  // Get the distance from this stop to all other reachable stops.
  $.ajax({
    type: 'GET',
    url: '/rpc?stopid='+this.stopid,
    success: plotStopDistance,
    datatType: 'json'
  });
};

/**
 * Permanently plots all the reachable stops from a clicked stop and colors them
 * based on how far away they are.
 */
var plotStopDistance = function(data) {
  var distance_results = JSON.parse(data);
  var businessList = [];
  distance_results.forEach(function(d) {
    d.stop_id = parseInt(d.stop_id, 10);
    d.seconds = parseInt(d.seconds, 10);

    // Update the marker.
    var marker = markerMap[d.stop_id];
    if (marker) {
      marker.icon.strokeColor = stopColor(d.seconds);
      marker.setMap(map);

      // Add the marker as being displayed.
      marker.is_displayed = true;
      displayList.push(marker);
    }

    /*
    var businesses = stop_business_list = businessMap[d.stop_id];
    for (var b = 0; b < businesses.length; ++b) {
      var business = businesses[b];
    }
    */
  });

  var distanceFilter = crossfilter(distance_results),
      minuteDimension = distanceFilter.dimension(function(d) { return Math.ceil(d.seconds / 60); });
      minuteGroup = minuteDimension.group();

  traveltimeChart
    .width(650)
    .height(300)
    .dimension(minuteDimension)
    .group(minuteGroup)
    .elasticY(true)
    .x(d3.scale.linear().domain([0, 100]))
    .xAxis();

  dc.renderAll();
};

/**
 * Returns a tile key for the current latitude and longitude.
 */
var getTileKey = function(latitutude, longitude) {
  return [Math.ceil(latitutude * tileBinSize), Math.ceil(longitude * tileBinSize)];
};

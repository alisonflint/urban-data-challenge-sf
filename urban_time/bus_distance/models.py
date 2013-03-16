from django.db import models
from bus_distance.distance import StopDistance  

def computeDistance(stopid):
  print "Getting data for: ", stopid
  stops = stop_distance_model.reach_search(stopid, 3, 60)
  print "Stops acquired"

  results = []
  for (stop_id, travel_time) in stops:
    results.append({"stop_id": stop_id, "seconds": travel_time})
  return results

stop_distance_model = StopDistance('bus_distance/static/passenger-count.csv')
stop_distance_model.set_time_range(1, 0, 24*60*60)

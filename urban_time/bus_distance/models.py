from django.db import models
import bus_distance.distance.StopDistance  

def computeDistance(stopid):
  stops = stop_distance_model.get_reach_for_stop(stopid)

  stop_ids = []
  travel_times = []
  for (stop_id, travel_time) in stops:
    stop_ids.append(stop_id)
    travel_times.append(travel_time)

  return (stop_ids, travel_times)

stop_distance_model = StopDistance('bus_distance/static/passenger-count.csv')

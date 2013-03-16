# Example calls:
# stop_distance_model=distance.StopDistance(fname)

# day = 1; starttime=0; endtime=12*60*60
# stop_distance_model.set_time_range(day, starttime, endtime)  

## depth is number of transition stops allowed
# start_stopID = 3377; depth=2; transition_time=5*60   
# stop_distance_model.reach_search(start_stopID, depth, transition_time)
# To run in command line:
# python
# import distance
# ds=distance.StopDistance('../../orgdata/public-transportation/san-francisco/passenger-count.csv')
# ds.set_time_range(1, 0, 24*60*60)
# ds.reach_search(3533, 3, 60)

import csv
import json
import numpy
import random
import time
from math import radians, sin, cos, asin, sqrt, pi, atan2

LARGE=-1

earth_radius_miles = 3956.0
def geo_distance(geo1, geo2):
  return abs(geo1[0]-geo2[0])*70+abs(geo1[1]-geo2[1])*55

def geo_distance_true(geo1, geo2):
  dlat = numpy.radians(geo1[0]) - numpy.radians(geo2[0])
  dlon = numpy.radians(geo1[1]) - numpy.radians(geo2[1])
  a = numpy.square(numpy.sin(dlat/2.0)) + cos(radians(geo2[0])) * numpy.cos(numpy.radians(geo1[0])) * numpy.square(numpy.sin(dlon/2.0))
  great_circle_distance = 2 * numpy.arcsin(numpy.sqrt(a))
  d = earth_radius_miles * great_circle_distance
  return d

class DistanceMatrix():
  def __init__(self, stop, trip, route, distance_computer):
    self.stop = stop
    self.trip = trip
    self.route = route
    self.time_matrix = {}
    self.distance_computer = distance_computer
    self.updateTimeMatrix()

  def updateTimeMatrix(self):
    # TIMING_triptime=0
    # TIMING_matrix=0
    timeMatrix={}
    self.time_matrix = {}
    for s0 in self.stop:
      self.time_matrix[s0]={}
      timeMatrix[s0]={}
      for s1 in self.stop:
        self.time_matrix[s0][s1]=[]
        timeMatrix[s0][s1]=[]
    for trip_id in self.trip:
      # tc0 = time.time()
      triptime = self.distance_computer.getTripTime(trip_id, self.route)
      # tc1 = time.time(); TIMING_triptime+=(tc1-tc0); tc0=tc1
      for t0 in triptime:
        for t1 in triptime:
          diff = t1[1]-t0[1]
          if (diff>0):
            timeMatrix[t0[0]][t1[0]].append(diff)
      # tc1 = time.time(); TIMING_matrix+=(tc1-tc0); tc0=tc1
    for s0 in self.stop:
      for s1 in self.stop:
        arr=timeMatrix[s0][s1]
        if (len(arr)==0):
          self.time_matrix[s0][s1]=LARGE
        else:
          self.time_matrix[s0][s1]=numpy.median(arr)
    for s0 in self.stop:
      self.time_matrix[s0][s0]=0
    # print "triptime uses "+str(TIMING_triptime)
    # print "matrix uses " + str(TIMING_matrix)

class StopDistance:
  def __init__(self, data_file):
    # reading data from csv
    self.data=[]
    i=0
    with open(data_file, 'rb') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',')
      for row in spamreader:
        self.data.append([])
        for ele in row:
          self.data[i].append(ele)
        i=i+1

    # getting the column names from data file
    i=0
    self.hd={}
    for ele in self.data[0]:
      self.hd[ele.lower()]=i
      i=i+1

    # Compute the set of unique routes for each stop.
    stops_array = {}
    geo_array = {}
    for row in self.data[1:-1]:
      if row[self.hd['day']] == '1':
        stop_id = int(row[self.hd['stop_id']])
        route = int(row[self.hd['route']])

        if stop_id in stops_array:
          route_set = stops_array[stop_id]
        else:
          route_set = set()
          stops_array[stop_id] = route_set
        route_set.add(route)
        geo_array[stop_id]=[float(row[self.hd['latitude']]), float(row[self.hd['longitude']])]

    print len(geo_array)
    
    self.neighbor_stops = {}
    for stop_id in stops_array:
      self.neighbor_stops[stop_id]=set()
      for stop_id_b in stops_array:
        if stop_id_b != stop_id:
          dist = geo_distance(geo_array[stop_id], geo_array[stop_id_b])
          if dist < 0.1: #this is the walking distance allowed for transfer, in mile
            self.neighbor_stops[stop_id].add(stop_id_b)

    # print neighbor_stops

    # Convert each set of routes into a list.
    for stop_id in stops_array:
      stops_array[stop_id] = list(stops_array[stop_id])

    self.routes=set()
    self.stop_ids=set()
    self.trip_ids=set()
    for row in self.data[1:]:
      self.routes.add(int(row[self.hd['route']]))
      self.stop_ids.add(int(row[self.hd['stop_id']]))
      self.trip_ids.add(int(row[self.hd['trip_id']]))

    self.routes = list(self.routes)
    self.stop_ids = list(self.stop_ids)
    self.trip_ids = list(self.trip_ids)
    self.stops_info = stops_array

    #separating data by route then by trip for speed
    self.databyroute={}
    for route in self.routes:
      self.databyroute[route]={}

    for ele in self.data[1:-1]:
      route=int(ele[self.hd['route']])
      trip = int(ele[self.hd['trip_id']])
      if trip in self.databyroute[route]:
        self.databyroute[route][trip].append(ele)
      else:
        self.databyroute[route][trip] = [ele]

  # find stops for given route
  def stopsForRoute(self, route_id):
    items=[]
    for trip in self.databyroute[route_id]:
      for ele in self.databyroute[route_id][trip]:
        if(int(ele[self.hd['route']])==route_id):
          items.append(int(ele[self.hd['stop_id']]))
    items=list(set(items))
    items.sort()
    return items

  # return [stop, time] list sorted ascending order
  def getTripTime(self, trip_id, route):
    triptime=[]
    for ele in self.databyroute[route][trip_id]:
      triptime.append([int(ele[self.hd['stop_id']]), self.time2num(ele[self.hd['timestop']])])
    return sorted(triptime, key=lambda x: x[1])

  def time2num(self, t):
    tarray=map(int, t.split(':'))
    return tarray[0]*60*60+tarray[1]*60+tarray[2]

  #find trips for route and day and time
  def getTripsForRoute(self, route, day, starttime, endtime):
    items=[]
    for trip_id in self.databyroute[route]:
      for ele in self.databyroute[route][trip_id]:
        if (ele[self.hd['day']]==str(day) and
            self.time2num(ele[15])>=starttime and
            self.time2num(ele[15])<endtime):
            items.append(int(ele[self.hd['trip_id']]))
    items=list(set(items))
    items.sort()
    return items

  def get_routes_for_stop(self, stop_id):
    if stop_id in self.stops_info:
      return self.stops_info[stop_id]
    else:
      return []

  #interface function, time unit is second
  def set_time_range(self, day, starttime, endtime):
    # print "enter set_time_range, updating routesArray"
    self.routesArray={}
    for route in self.routes:
      self.routesArray[route] = DistanceMatrix(
          self.stopsForRoute(route),
          self.getTripsForRoute(route, day, starttime, endtime),
          route,
          self)
    return "done"

  #interface function, given stop_d return list of stops reachable and the time to get there
  def get_reach_for_stop(self, stop_id):
    # pdb.set_trace()
    report={}
    for route in self.get_routes_for_stop(stop_id):
      time_matrix = self.routesArray[route].time_matrix
      tm = time_matrix
      reaches = dict((k, v) for k, v in time_matrix[stop_id].items() if v>0)
      report = dict(report.items()+reaches.items())
    return sorted(report.iteritems(), key=lambda x: x[1])

  # used for reach_search. don't call directly
  def single_reach_from_stop(self, stop_id, starttime):
    # global reached_routes, reached_stops, reach_time
    route_list = self.get_routes_for_stop(stop_id)
    # print route_list
    route_list = list(set(route_list)-set(self.reached_routes))
    self.reached_routes = list(set(route_list) | set(self.reached_routes)) #add new routes to the reached_routes list
    reaches={}
    for route in route_list:
      this_reach = dict((k, v) for k, v in self.routesArray[route].time_matrix[stop_id].items() if v>0)
      reaches = dict(reaches.items()+this_reach.items()) #each item : {stop: time}
    for reach in reaches:
      if not(reach in self.reached_stops):   # a new stop reached
        self.reached_stops.append(reach)
        self.reach_time.append([reach, reaches[reach]+starttime])
    if stop_id in self.neighbor_stops:
      for neighbor in self.neighbor_stops[stop_id]:
        if not(neighbor in self.reached_stops):
          self.reach_time.append([neighbor, starttime+8*60])
          self.reached_stops.append(neighbor)
    self.reach_time = sorted(self.reach_time, key=lambda x: x[1])

  # depth is number of changes allowed.
  def reach_search(self, starting_stop_id, depth, transition_time):
    # global reached_routes, reached_stops, reach_time
    self.reached_stops=[]
    self.reached_routes=[]
    self.reach_time=[]
    self.reached_stops.append(starting_stop_id)
    self.single_reach_from_stop(starting_stop_id, 0)
    while (depth>0):
      for reach in self.reach_time:
        self.single_reach_from_stop(reach[0], 5*60)
      depth -= 1
    return self.reach_time


if __name__ == "__main__":
  import sys
  stop_distance = StopDistance(sys.argv[1])

# StopDistance('../../orgdata/public-transportation/san-francisco/passenger-count.csv')

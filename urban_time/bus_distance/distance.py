import csv
import json
import numpy
import random
import time

LARGE=-1

class DistanceMatrix():
  def __init__(self, stop, trip, route, distance_computer):
    self.stop = stop
    self.trip = trip
    self.route = route
    self.time_matrix = {}
    self.distance_computer = distance_computer
    self.updateTimeMatrix()

  def updateTimeMatrix(self):
    TIMING_triptime=0
    TIMING_matrix=0
    timeMatrix={}
    self.time_matrix = {}
    for s0 in self.stop:
      self.time_matrix[s0]={}
      timeMatrix[s0]={}
      for s1 in self.stop:
        self.time_matrix[s0][s1]=[]
        timeMatrix[s0][s1]=[]
    for trip_id in self.trip:
      tc0 = time.time()
      triptime = self.distance_computer.getTripTime(trip_id, self.route)
      tc1 = time.time(); TIMING_triptime+=(tc1-tc0); tc0=tc1
      for t0 in triptime:
        for t1 in triptime:
          diff = t1[1]-t0[1]
          if (diff>0):
            timeMatrix[t0[0]][t1[0]].append(diff)
      tc1 = time.time(); TIMING_matrix+=(tc1-tc0); tc0=tc1
    for s0 in self.stop:
      for s1 in self.stop:
        arr=timeMatrix[s0][s1]
        if (len(arr)==0):
          self.time_matrix[s0][s1]=LARGE
        else:
          self.time_matrix[s0][s1]=numpy.median(arr)
    for s0 in self.stop:
      self.time_matrix[s0][s0]=0
    print "triptime uses "+str(TIMING_triptime)
    print "matrix uses " + str(TIMING_matrix)

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

    #separating data by route for speed
    self.databyroute={}
    for route in self.routes:
      self.databyroute[route]=[]

    for ele in self.data[1:-1]:
      route=int(ele[self.hd['route']])
      self.databyroute[route].append(ele)

  # find stops for given route
  def stopsForRoute(self, route_id):
    items=[]
    for ele in self.databyroute[route_id]:
      if(int(ele[self.hd['route']])==route_id):
        items.append(int(ele[self.hd['stop_id']]))
    items=list(set(items))
    items.sort()
    return items

  def getTripTime(self, trip_id, route):
    triptime=[]
    for ele in self.databyroute[route]:
      if int(ele[self.hd['trip_id']])==trip_id:
        triptime.append([int(ele[self.hd['stop_id']]), self.time2num(ele[15])])
    return triptime

  def time2num(self, t):
    tarray=map(int, t.split(':'))
    return tarray[0]*60*60+tarray[1]*60+tarray[2]

  #find trips for route and day and time
  def getTripsForRoute(self, route, day, starttime, endtime):
    items=[]
    for ele in self.databyroute[route]:
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
    print "enter set_time_range, updating routesArray"
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

if __name__ == "__main__":
  import sys
  stop_distance = StopDistance(sys.argv[1])

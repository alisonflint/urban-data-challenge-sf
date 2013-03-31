import csv
import os
import sys

from heapq import heappush, heappop

class TransitGraph:
  def __init__(self, transit_graph_file):
    csvfile = csv.reader(open(transit_graph_file, 'r'))
    self.transit_graph = {}
    csvfile.next()
    self.stopset = set()
    for row in csvfile:
      stop1, stop2, arrive_time, travel_time = row
      stop1 = int(stop1)
      stop2 = int(stop2)
      travel_time = int(travel_time)

      self.stopset.add(stop1)
      self.stopset.add(stop2)

      if stop1 not in self.transit_graph:
        stop_list = {}
        self.transit_graph[stop1] = stop_list
      else:
        stop_list = self.transit_graph[stop1]
      
      if stop2 not in stop_list:
        link_list = []
        stop_list[stop2] = link_list
      else:
        link_list = stop_list[stop2]

      link_list.append(travel_time)

    # Convert each edge list into an average number of seconds between each
    # stop.
    for stop1_id in self.transit_graph:
      stop_list = self.transit_graph[stop1_id]
      for stop2_id in stop_list:
        travel_list = stop_list[stop2_id]
        stop_list[stop2_id] = sum(travel_list) / float(len(travel_list))

  def getShortestDistance(self, source):
    dist = {}
    for stopid in self.stopset:
      dist[stopid] = sys.float_info.max
    dist[source] = 0

    q = []
    for stopid in dist:
      heappush(q, (dist[stopid], stopid))

    while (len(q) > 0):
      best_in_q = heappop(q)
      print "top in heap:", best_in_q
      if best_in_q[0] == sys.float_info.max:
        break

      stop_list = self.transit_graph.get(best_in_q[1], [])
      print "stop_list:", stop_list
      for neighbor in stop_list:
        travel_time = stop_list[neighbor]
        alt = travel_time + best_in_q[0]
        if alt < 0:
          print alt
          sys.exit(1)
        if alt < dist[neighbor]:
          dist[neighbor] = alt
          for i in xrange(0, len(q)):
            if q[i][1] == neighbor:
              del q[i]
              break
          heappush(q, (dist[neighbor], neighbor))
    return [ (stop, time) for (stop, time) in dist.iteritems()
                          if time < sys.float_info.max ]
          
if __name__ == "__main__":
  transit_graph = TransitGraph(sys.argv[1])
  print "loaded transit_graph"
  distance_map = transit_graph.getShortestDistance(3893)
  print len(reachable_stops)
  print reachable_stops

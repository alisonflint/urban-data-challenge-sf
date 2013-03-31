
import csv 
import json 
import gzip
import sys 

from datetime import datetime

STOPID = 1
ON = 3
OFF = 4
LOAD = 5
MONTH = 6
DAY = 7
YEAR = 8
TIMESTOP = 15
TIMEDOORCLOSE = 16
TIMEPULLOUT = 17
TRIPID = 18
DATE_FMT = "%H:%M:%S"

class TransitGraph():
  def __init__(self, passenger_count_file):
    csv_file = csv.reader(gzip.open(passenger_count_file, 'rb'))
    csv_lines = list(csv_file)
    print "stop1, stop2, arrive_time, travel_time"
    for i in xrange(1, len(csv_lines)-1):
      if (csv_lines[i][TRIPID] != csv_lines[i+1][TRIPID]):
        continue;

      base_stopid = int(csv_lines[i][STOPID])
      next_stopid = int(csv_lines[i+1][STOPID])

      full_arrive_time = "%s-%s-%s %s" %(
          csv_lines[i][YEAR],
          csv_lines[i][MONTH],
          csv_lines[i][DAY],
          csv_lines[i][TIMESTOP])

      base_arrive_time = csv_lines[i][TIMESTOP]
      base_arrive_s = self.convertTimeToSeconds(base_arrive_time)
      next_arrive_time = csv_lines[i+1][TIMESTOP]
      next_arrive_s = self.convertTimeToSeconds(next_arrive_time)

      travel_s = next_arrive_s - base_arrive_s
      print "%d, %d, %s, %d" %(
          base_stopid, next_stopid, full_arrive_time, travel_s)

  def convertTimeToSeconds(self, time_str):
    hour, minute, seconds = time_str.split(":")
    return int(seconds) + 60 * int(minute) + 60*60*int(hour)

if __name__ == "__main__":
  transit_graph = TransitGraph(sys.argv[1])


import csv 
import json 
import gzip
import sys 

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

def getGraphJson(passenger_count_file):
  csv_file = csv.reader(gzip.open(passenger_count_file, 'rb'))
  csv_lines = list(csv_file)
  node_map = {}
  link_set = set()
  node_index = 0
  for i in xrange(1, len(csv_lines)-1):
    if (csv_lines[i][TRIPID] != csv_lines[i+1][TRIPID]):
      continue;

    base_stopid = int(csv_lines[i][STOPID])
    next_stopid = int(csv_lines[i+1][STOPID])

    if base_stopid not in node_map:
      node_map[base_stopid] = node_index;
      node_index += 1;

    if next_stopid not in node_map:
      node_map[next_stopid] = node_index;
      node_index += 1;

    link_set.add((node_map[base_stopid], node_map[next_stopid]))

  links = []
  for source, target in link_set:
    links.append({"source": source, "target": target, "value": 1.0})

  nodes = []
  for node in node_map:
    nodes.append({"name": node})

  return {"nodes": list(nodes), "links": links}

if __name__ == "__main__":
  graph = getGraphJson(sys.argv[1])
  print json.dumps(graph, indent=2)

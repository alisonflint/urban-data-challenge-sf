# 0 STOP_SEQ
# 1 STOP_ID
# 2 STOP_NAME
# 3 ON
# 4 OFF
# 5 LOAD
# 6 MO
# 7 DAY
# 8 YR
# 9 ROUTE
# 10 LATITUDE
# 11 LONGITUDE
# 12 TRIP_ID
# 13 DIR
# 14 VEHNO
# 15 TIMESTOP
# 16 TIMEDOORCLOSE
# 17 TIMEPULLOUT
# 18 TRIPCODE
# 19 TRIPSTOP
# 20 DOORDWELL
# 21 WAITDWELL

import csv
import time
import numpy
import json

#reading data from csv
data=[]
i=0
with open('../orgdata/public-transportation/san-francisco/passenger-count.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		data.append([])
		for ele in row:
			data[i].append(ele)
		i=i+1

# getting the column names from data file
i=0
hd={}
for ele in data[0]:
	hd[ele.lower()]=i
	print i, ele
	i=i+1

def time2num(t):
	tarray=map(int, t.split(':'))
	return tarray[0]*60*60+tarray[1]*60+tarray[2]

#checking data
for ele in data:
	if ele[hd['route']]=='1' and ele[hd['day']]=='1':    # route 1, day 1
		print map(ele.__getitem__, (hd['stop_seq'], hd['stop_id'], hd['day'], hd['route'], hd['trip_id'], hd['timestop'])), time2num(ele[15])

#uniq route_stop pair, turned out multiple routes share same stops
stops_route=[]
for ele in data[1:-1]:
	if ele[hd['day']]=='1':    # route 1, day 1
		stops_route.append(ele[hd['stop_id']]+'_'+ele[hd['route']])

#finding uniq route, stop, trip_id, etc
def uniqueItems(item):
	items=[]
	for ele in data[1:-1]:
		items.append(ele[hd[item]])
	items=list(set(items))
	items.sort()
	return items

# lists of uniq items
routes=uniqueItems('route')
stop_ids=uniqueItems('stop_id')
trip_ids=uniqueItems('trip_id')
info={}
info['routes']=routes
info['stop_ids']=stop_ids
info['trip_ids']=trip_ids


#separating data by route for speed
databyroute={}
for route in routes:
	databyroute[route]=[]

for ele in data[1:-1]:
	route=ele[hd['route']]
	databyroute[route].append(ele)


#finding stops for given route
def stopsForRoute(route_id):
	items=[]
	for ele in databyroute[route_id]:
		if(ele[hd['route']]==route_id):
			items.append(ele[hd['stop_id']])
	items=list(set(items))
	items.sort()
	return items


#find trips for route and day and time
def getTripsForRoute(route, day, starttime, endtime):
	items=[]
	for ele in databyroute[route]:
		if(ele[hd['day']]==day and time2num(ele[15])>=starttime and time2num(ele[15])<endtime):
			items.append(ele[hd['trip_id']])
	items=list(set(items))
	items.sort()
	return items


# final out put area
# constructing a master array to hold stops and trips for each route at given day and hour range
day='1'
endtime=12*60*60
starttime=0

# now we calculating the master data set to be saved later
routesArray={}
for route in routes:
	routesArray[route]={}
	routesArray[route]['stop']=stopsForRoute(route)

for route in routes:
	routesArray[route]['trip']=getTripsForRoute(route, day, starttime, endtime)

def getTripTime(trip_id, route):
	triptime=[]
	for ele in databyroute[route]:
		if ele[hd['trip_id']]==trip_id:
			triptime.append([ele[hd['stop_id']], time2num(ele[15])])
	return triptime

LARGE=-1

def getRouteTimeMatrix(route):
	timeMatrix={}
	report={}
	stops = routesArray[route]['stop']
	for s0 in stops:
		report[s0]={}
		timeMatrix[s0]={}
		for s1 in stops:
			report[s0][s1]=[]
			timeMatrix[s0][s1]=[]
	for trip_id in routesArray[route]['trip']:
		triptime=getTripTime(trip_id, route)
		for t0 in triptime:
			for t1 in triptime:
				diff = t1[1]-t0[1]
				if (diff>0):
					timeMatrix[t0[0]][t1[0]].append(diff)
	for s0 in stops:
		for s1 in stops:
			arr=timeMatrix[s0][s1]
			if (len(arr)==0):
				# print s0+" "+s1+" is empty"
				report[s0][s1]=LARGE
			else:
				report[s0][s1]=numpy.median(arr)
	for s0 in stops:
		report[s0][s0]=0
	return report

for route in routes:
	routesArray[route]['timeMatrix']=getRouteTimeMatrix(route)

f=open('info.json', 'w')
f.write(json.dumps(info))
f.close()

f=open('day_1_hour_0_12.json', 'a')
f.write(json.dumps(routesArray))
f.close()




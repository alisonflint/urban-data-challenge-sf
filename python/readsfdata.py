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


for ele in data:
	if ele[hd['route']]=='1' and ele[hd['day']]=='1':    # route 1, day 1
		print map(ele.__getitem__, (hd['stop_seq'], hd['stop_id'], hd['day'], hd['route'], hd['trip_id'], hd['timestop'])), time2num(ele[15])

stops=[]
for ele in data[1:-1]:
	if ele[hd['day']]=='1':    # route 1, day 1
		stops.append(ele[hd['stop_id']]+'_'+ele[hd['route']])

def uniqueItems(item):
	items=[]
	for ele in data[1:-1]:
		items.append(ele[hd[item]])
	items=list(set(items))
	items.sort()
	return items

routes=uniqueItems('route')
stops=uniqueItems('stop')
trip_ids=uniqueItems('trip_id')



stops=list(set(stops))

		print map(ele.__getitem__, (hd['stop_seq'], hd['stop_id'], hd['day'], hd['route'], hd['trip_id'], hd['timestop'])), time2num(ele[15])




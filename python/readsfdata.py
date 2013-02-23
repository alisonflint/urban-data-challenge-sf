import csv
data=[]
i=0
with open('../orgdata/public-transportation/san-francisco/realtime-arrivals.excerpt.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		data.append([])
		for ele in row:
			data[i].append(ele)
		i=i+1


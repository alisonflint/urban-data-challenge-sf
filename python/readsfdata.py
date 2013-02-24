import csv
data=[]
i=0
with open('C:/Users/Alison/Documents/GitHub/urban-data-challenge-sf/data/passenger-count.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		data.append([])
		for ele in row:
			data[i].append(ele)
		i=i+1

data[0]
data[1]

header={}
i=0
for x in data[0]:
        print i, x
#        header.append(x)
        i=i+1


#data[0]

#def time2num(t):
#        tarray=map(int,t.split(':'))
#        return tarray[0]*60*60+tarray[1]*60+tarray[2]

#for ele in data:
 #       if ele[9]=='1' and ele[7]=='1':
  #              print map(ele.__getitem__,{0,1,7,9,12,15}),time2num(ele[15])
   #             stopsequence.append(ele.__getitem__,{0})
                

#min(stopsequence)

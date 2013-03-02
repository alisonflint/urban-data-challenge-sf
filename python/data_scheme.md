
under /pypthon
/python/readsfdata.py      #source script for processing the data
/python/info.json               #json with lists for route, stop_id, and trip_id
/python/day_1_hour_0_12.json          #The timeMatrix


info.json:
{ 'routes': ['1', '5', '10'...],                              # All the routes in the city of SF, routes may change stops depending on time of the day
  'stop_ids': ['1234', '3452',...],                    # All the stops in the city. Many stops are shared between routes
   'trip_ids': ['345', '2344', '3444', ...]}          # All the trips 

day_1_hour_0_12.json                             # day 1, from 0 to 12 hour
{   route1 : { 'stop': ['2134', '3334', ...],          
                  'trip': ['345', 22344', ...],
                  'timeMatrix': {stop0: {{stop0, time00}, {stop1, time01}, {stop2, time02}, ...},
                                         stop1: {{stop0, time10}, {stop1, time11}, {stop2, time12}, ...},
                                         stop2: {{stop0, time20}, {stop1, time21}, {stop2, time22}, ...},
                                         ...},
    route2 : { 'stop': ['2134', '3334', ...],          
                  'trip': ['345', 22344', ...],
                  'timeMatrix': {stop0: {{stop0, time00}, {stop1, time01}, {stop2, time02}, ...},
                                         stop1: {{stop0, time10}, {stop1, time11}, {stop2, time12}, ...},
                                         stop2: {{stop0, time20}, {stop1, time21}, {stop2, time22}, ...},
                                         ...},
 ...}

 
So let's see if you want to get time to travel to all the connected stops from stop '1234' of route '12' during the first 12 hours of day1:
timeMatrix=load_json_function('day_1_hour_0_12.json.json')
expected_travel_time_hash = timeMatrix['12']['timeMatrix']['1234']

which will return a hash of:
{{stop0, time0}, {stop1, time1},...}
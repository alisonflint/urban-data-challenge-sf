from django.db import models
import json

# Load the initial matrix
test_list = json.load(open("bus_distance/static/arrivals.json", 'r'))

# On a call, filter the time frames we care about and then re-average everything

# Then return the list of things that are important.

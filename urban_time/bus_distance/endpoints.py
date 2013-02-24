from django.views.decorators.csrf import csrf_exempt
from ajax import endpoint
from ajax.decorators import login_required
from ajax.endpoints import ModelEndpoint
from ajax.exceptions import AJAXError
from bus_distance.models import test_list, computeDistance

@csrf_exempt
def right_back_at_you(request):
  print request.POST['name']
  print request.POST['age']
  print test_list
  if len(request.POST):
    return request.POST
  else:
    raise AJAXError(500, 'Nothing to echo back.')

@csrf_exempt
def distance(request):
  (stops, times) = computeDistance(int(request.POST['stopid']))
  stoptimes = []
  for i in range(len(stops)):
    stoptimes.append({"stopid": stops[i], "time": times[i]})
  return stoptimes


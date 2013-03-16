from django.views.decorators.csrf import csrf_exempt
from ajax import endpoint
from ajax.decorators import login_required
from ajax.endpoints import ModelEndpoint
from ajax.exceptions import AJAXError
from bus_distance.models import computeDistance

@csrf_exempt
def distance(request):
  return {"results": computeDistance(int(request.POST['stopid']))}

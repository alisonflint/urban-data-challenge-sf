# Create your views here.

from django.template import Context, loader
from django.http import HttpResponse
from bus_distance.models import test_list

def index(request):
  print "Received"
  c = Context({})
  return HttpResponse(loader.get_template('bus_distance/index.html').render(c))

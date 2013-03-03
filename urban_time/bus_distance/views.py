# Create your views here.

from django.template import Context, loader
from django.http import HttpResponse

def index(request):
  c = Context({})
  return HttpResponse(loader.get_template('bus_distance/index.html').render(c))

from django.shortcuts import render
import computerInfo
import json
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request,'index.html')

def getBrandPie(request):
    brands=computerInfo.getBrand()
    return HttpResponse(json.dumps(brands), content_type="application/json")

def getBrandBar(request):
    bar=computerInfo.getBar()
    return HttpResponse(json.dumps(bar), content_type="application/json")

def getParseVideo(request):
    print(request.POST)
    realStie={
        'realSite': 'baidu.com'
    }
    return HttpResponse(json.dumps(realStie), content_type="application/json")
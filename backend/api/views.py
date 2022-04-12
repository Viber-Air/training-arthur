from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Acceleration
import json
import re

models = {'acceleration': Acceleration}

def index(request):
    return render(request, 'index.html')

def api(request, **kwargs):
    match request.method:
        case 'GET':
            return api_get(request, kwargs)
        case 'POST':
            return api_post(request, kwargs)

def api_get(request, kwargs):
    #Lembrete: collection(MongoDB) = model(Django)
    model = models[kwargs['collection'].lower()] 
    filters = parse_filters(request)

    resp = {}
    for item in model.objects.filter(**filters):
        d = item.to_dict()
        resp[d['id']] = d

    return JsonResponse(resp)

def api_post(request, kwargs):
    model = models[kwargs['collection'].lower()]
    data = json.loads(request.body)
   
    filters = parse_filters(request)
 
    query = model.objects.filter(**filters)
    if query.exists() and bool(filters):
        query.update(**data)
    else:
        new_entry = model(**data)
        new_entry.save()
    
    return api_get(request, kwargs)
    #return JsonResponse(data)

def parse_filters(request):
    values = request.GET

    filters = {}
    for i in values:
        value = values[i]
        if re.match( r'^\((\w+,)+\w+\)$', value):
            filters[i] = value[1:-1].split(',')
        else:
            filters[i] = value

        #Falta tratar datetime aqui
    return filters

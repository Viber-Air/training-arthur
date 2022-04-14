from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from .models import RawData
from bson.objectid import ObjectId
from datetime import datetime
import json
import re

models = {'rawdata':RawData}

def index(request):
    return render(request, 'index.html')

def api(request, **kwargs):
    if request.method == 'GET':
        return api_get(request, kwargs)
    elif request.method == 'POST':
        return api_post(request, kwargs)
    raise Http404(f'Method {request.method} not implemented!')
    

def api_get(request, kwargs):
    #Lembrete: collection(MongoDB) = model(Django)
    model = models[kwargs['collection'].lower()] 
    filters = parse_filters(request)

    resp = {}
    for item in model.objects.filter(**filters):
        d = item.to_dict()
        resp[d['_id']] = d

    return JsonResponse(resp)


def api_post(request, kwargs):
    model = models[kwargs['collection'].lower()]
    data = json.loads(request.body)
    filters = parse_filters(request)

    #Caso seja enviado um filtro e exista algum valor correspondente,
    #os documentos são atualizados
    query = model.objects.filter(**filters)
    if query.exists() and bool(filters):
        query.update(**data)
    else:
        new_entry = model(**data)
        new_entry.save()

    # Retorna uma query com os mesmos parametros para conferência
    return api_get(request, kwargs)


def parse_filters(request):
    filters = {}
    for key, value in request.GET.items():
        # Tratando ranges
        if re.match( r'^\((.+,)+.+\)$', value):
            value_list = value[1:-1].split(',')
            filters[key] = [correct_datatypes(key, v) for v in value_list]
        else:
            filters[key] = correct_datatypes(key, value)
    return filters


def correct_datatypes(key, value):
    # ObjectIdField
    if key == '_id':
        return ObjectId(value)
    return value

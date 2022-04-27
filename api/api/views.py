from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import RawData, Sensor
from .serializers import RawDataSerializer, SensorSerializer
from bson import ObjectId
import re

MODELS = {
        'rawdata': RawData,
        'sensor' : Sensor,
        }

SERIALIZERS = {
        'rawdata': RawDataSerializer,
        'sensor' : SensorSerializer
        }


def index(request):
    return render(request, 'index.html')


@api_view(['GET', 'PUT', 'POST', 'DELETE'])
def api(request, collection):
    Model = MODELS[collection.lower()]
    Serializer = SERIALIZERS[collection.lower()]
    filters,order_by = parse_params(request, Model)
    data = parse_data(request)

    if request.method == 'GET':
        query = Model.objects.filter(**filters).order_by(*order_by)
        resp = Serializer(query, many=True)

    elif request.method == 'POST':
        resp = Serializer(data=data, many=True)
        if resp.is_valid():
            resp.save()
        else:
            return Response(status=400)

    elif request.method == 'PUT':
        query = Model.objects.get(pk = ObjectId(data[0]['_id']))
        resp = Serializer(query, data=data[0])
        if resp.is_valid():
            resp.save()
        else:
            return Response(status=400)

    elif request.method == 'DELETE':
        # CUIDADO: TODOS OS MATCHES SERÃO APAGADOS!
        if len(filters)>0:
            query = Model.objects.filter(**filters)
            for item in query:
                item.delete()
        query = Model.objects.filter(**filters)
        resp = Serializer(query, many=True)

    return Response(resp.data)


def parse_params(request, Model):
    params = {}
    filters = {}
    order_by = []

    #Tratando os valores recebidos
    for key, value in request.GET.items():  
        if re.match( r'^\((.+,)+.+\)$', value):
            value_list = value[1:-1].split(',')
            params[key] = value_list
        else:
            params[key] = value

    #Separando os campos (filters,order_by,etc...)
    keys = list(params.keys())
    for key in keys:
        if key in Model.__dict__:
            filters[key] = params[key]

        elif key == 'order_by':
            if type(params[key]) is list:
                order_by = params[key]
            else:
                order_by = [params[key]]

    return filters,order_by

def parse_data(request):
    if type(request.data) is dict:
        return [request.data]
    return request.data
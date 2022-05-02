# Setup
Using Linux or WSL:

## Running
'''bash
git clone git@github.com:alom101/WP-API.git
cd WP-API
sudo docker-compose up --build -d
'''

## Adding a super user
'''bash
sudo docker exec -it api sh
python api/manage.py createsuperuser
'''


# Usage:

## TLDR
The api is based on a call to Django's QuerySet.filter() then QuerySet.order_by(). Every keyword comes from there, i.e.:

gt | greater than
gte | greater than or equal to
lt | less than
lte | less than or equal to
range(   ,   ) | range test (inclusive)

__POST and PUT requests don't accept any filter or order, DELETE accepts filters and GET accepts filters and order__


## URL format:
'''
http://IP:PORT/api/COLLECTION/?[FILTERS & ORDER_BY]
'''
Where everything after "?" is optional

For the examples we'll use the rawdata collection. So the base url will look like: http://localhost:8000/

### Filtering
Getting | URL
All data | /api/rawdata
All data from sensor S1 | /api/rawdata/?sensor_id=S1
All data from 01/04/22 | /api/rawdata/?initial_time__gt=2022-04-01
All data until 01/04/22 | /api/rawdata/?initial_time__lt=2022-04-01
All data from 01/04/22 12:30:00 | /api/rawdata/?initial_time__gt=2022-04-01T12:30:00
All data from 01/04/22 to 01/05/22 | /api/rawdata/?initial_time__range=(2022-04-01,2022-05-01)

### Ordering
Ordering by | URL
sensor_id | /api/rawdata/?order_by=sensor_id
sensor_id then initial_time | /api/rawdata/?order_by=(sensor_id,initial_time)

### More complex queries
All requests above can be mixed:

> Getting only data from sensor S1 and from 01/04/22:
> /api/rawdata/?sensor_id=S1&initial_time__gt=2022-04-01

> Getting only data from sensor S1 and ordering by initial_time:
> /api/rawdata/?sensor_id=S1&order_by=initial_time


## Examples with Python Requests

### POST new sensor
'''python
import requests
import json

url = "http://localhost:8000/api/sensor/"

payload = json.dumps({
  "_id": "626860c851d908b99ec72a46",
  "name": "Celular1",
  "location": "Sala da WP",
  "_type": "Accelerometer",
  "description": "Acelerometro do celular1"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
'''

### POST new rawdata 
'''python
import requests
import json

url = "http://localhost:8000/api/rawdata/"

payload = json.dumps({
  "sensor": "Celular1",
  "initial_time": "2022-04-20 18:47:35",
  "final_time": "2022-04-20 18:47:35",
  "values": [
    {
      "_time": "2022-04-20 18:47:35",
      "value": "1"
    },
    {
      "_time": "2022-04-20 18:48:35",
      "value": "2"
    },
    {
      "_time": "2022-04-20 18:49:35",
      "value": "3"
    }
  ]
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

'''

### POST multiple new sensors
'''python
import requests
import json

url = "http://localhost:8000/api/sensor/"

payload = json.dumps([
  {
    "_id": "6268682d46ea7f063fa90acb",
    "name": "Celular2",
    "location": "Sala da WP",
    "_type": "Accelerometer",
    "description": "Acelerometro do celular2"
  },
  {
    "_id": "6268682d46ea7f063fa90acc",
    "name": "Celular3",
    "location": "Sala da WP",
    "_type": "Accelerometer",
    "description": "Acelerometro do celular3"
  }
])
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
'''


### GET all sensors
'''python
import requests

url = "http://localhost:8000/api/sensor/"

response = requests.get(url)

print(response.text)
'''


### GET all rawdata
'''python
import requests

url = "http://localhost:8000/api/rawdata/"

response = requests.get(url)

print(response.text)
'''

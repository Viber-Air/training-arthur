from djongo import models

# Create your models here.


class Sensor(models.Model):
    _id = models.ObjectIdField(unique=True)
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    _type = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    
    def __str__(self):
    def to_dict(self):
        resp = {}
        resp['_id'] = str(self.id)
        resp['location'] = self.location
        resp['_type'] = self.type
        return resp
        return f'{self.name} at {self.location}'


class RawData(models.Model):
    _id = models.ObjectIdField()
    sensor_id = models.ForeignKey('Sensor', on_delete=models.CASCADE, to_field='name')
    initial_time = models.DateTimeField()
    final_time = models.DateTimeField()
    values = models.FloatField()

    def __str__(self):
        return f'Data from {self.sensor_id} collected from {self.initial_time} to {self.final_time}'

    def to_dict(self):
        resp = {}
        resp['_id'] = str(self._id)
        resp['sensor_id'] = self.sensor_id
        resp['initial_time'] = self.initial_time
        resp['final_time'] = self.final_time
        resp['values'] = self.values
        return resp



from djongo import models

# Create your models here.


class Sensor(models.Model):
    _id = models.ObjectIdField(unique=True)
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    _type = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    
    def __str__(self):
        return f'{self.name} at {self.location}'


class Measure(models.Model):
    _time = models.DateTimeField()
    value = models.FloatField()

    class Meta:
        abstract = True


class RawData(models.Model):
    _id = models.ObjectIdField()
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, to_field='name')
    initial_time = models.DateTimeField()
    final_time = models.DateTimeField()
    values = models.ArrayField( model_container=Measure)

    def __str__(self):
        return f'Data from {self.sensor_id} collected from {self.initial_time} to {self.final_time}'

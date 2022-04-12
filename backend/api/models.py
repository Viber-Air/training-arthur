from djongo import models
import json
# Create your models here.

class Acceleration(models.Model):
    absolute_time = models.TimeField()
    relative_time = models.TimeField()
    acc_x = models.FloatField()
    acc_y = models.FloatField()
    acc_z = models.FloatField()
    acc = models.FloatField()

    def __repr__(self):
        return str(self.absolute_time) + ' ' + str(self.acc)
  
    def to_dict(self):
        resp = {}
        resp['id'] = self.id
        resp['absolute_time'] = self.absolute_time
        resp['relative_time'] = self.relative_time
        resp['acc_x'] = self.acc_x
        resp['acc_y'] = self.acc_y
        resp['acc_z'] = self.acc_z
        resp['acc'] = self.acc
        return resp

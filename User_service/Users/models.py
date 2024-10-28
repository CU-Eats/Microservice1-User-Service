from django.db import models

# Create your models here.
class users(models.Model):
    uni = models.IntegerField()
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    ID_TYPE_CHOICES = [ ('student', 'Student'), ('faculty', 'Faculty'), ('guest', 'Guest'), ]
    id_type = models.CharField(max_length=10, choices=ID_TYPE_CHOICES)

def __str__(self):
    return f"{self.first_name} - {self.last_name} - {self.uni}"
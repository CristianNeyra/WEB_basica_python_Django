from django.db import models

# Create your models here.
class paciente(models.Model):
    rut = models.CharField(max_length=12, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.IntegerField()

class doctor(models.Model):
    iddoctor = models.CharField(max_length=10)
    nombre_doctor = models.CharField(max_length=100)
    profesion = models.CharField(max_length=50)
    apodo = models.CharField(max_length=50)
    rut_paciente = models.ForeignKey('paciente', on_delete=models.CASCADE)

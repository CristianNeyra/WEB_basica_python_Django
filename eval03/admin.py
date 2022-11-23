from django.contrib import admin
from eval03.models import paciente, doctor

class pacienteAdmin(admin.ModelAdmin):
    list_display = ("rut", "nombre","apellido", "email","telefono")
    search_fields = ("rut", "nombre")

class doctorAdmin(admin.ModelAdmin):
    list_display = ("iddoctor","nombre_doctor","profesion","apodo","rut_paciente")
    search_fields = ("nombre_doctor", "profesion", "apodo")

admin.site.register(paciente, pacienteAdmin)
admin.site.register(doctor, doctorAdmin)

# Register your models here.

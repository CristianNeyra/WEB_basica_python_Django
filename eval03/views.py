from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context
from django.core.mail import send_mail
from django.template.context import RequestContext
import pandas
from eval03.models import *
from Cristian_Neyra import settings
from django_pandas.io import *

# Create your views here.
def inicio(request): #primera vista
    return render(request, "miplantilla.html")
    
def requerimiento01(request): #vista del primer requerimiento
    return render(request, "requerimiento01.html")

def requerimiento02(request): #vista del primer requerimiento
    return render(request, "requerimiento02.html")

def requerimiento03(request): #vista del tercer requerimiento
    #Se realiza la consulta para obtener todos los elementos de la tabla paciente
    pacientes = paciente.objects.order_by('rut')
    #Se retorna la lista de resultados RS a la vista
    return render(request, "requerimiento03.html", {"lista":pacientes})

def buscar(request): #vista de la busqieda de pacientes por el nombre, carga el resultado en la vista
    if request.GET["paciente"]:
        #Se asocian las variables que llegan por metodo GET
        p = request.GET["paciente"]
        #Se efectua la busqueda en la BD
        pacientesresultado = paciente.objects.filter(nombre__icontains=p)
        #Se retorna la lista de rsultado RS a la vista
        return render(request, "resultado.html", {"paciente":p, "lista":pacientesresultado})
    else:
        mensaje = "No se ha introducido un nombre"
    return HttpResponse(mensaje)

def correoelectronico(request): #proceso de envio de mail y carga la vista de confirmación en caso de error manda mensaje por response
       
    if request.method == "POST":
        #se asocian las variables que llegan mediante evento POST
        nombre = request.POST['nombre']
        email_destinatario = request.POST['email']
        asunto = request.POST['asunto']
        cuerpo = request.POST['mensaje']
        email_from = settings.EMAIL_HOST_USER
        mensaje = "Estimado Sr(a). " + str(nombre) + ": "+ str(cuerpo)
        #se envia el correo electronico
        send_mail(
            asunto,
            mensaje,
            email_from,
            [email_destinatario],
            fail_silently=False,
        )
        return render(request, "correo.html")
    else:
        mensaje = "No se ha podido realizar el envio del email, intente nuevamente"
    return HttpResponse(mensaje)

def correomasivo(request): #recive un archivo CVS con los datos para enviar los correos de manera masiva
    if request.method == "POST":
        #Se asocia la varieble recivida por metodo POST
        csv = request.FILES['csvsubido']
        #Se parametriza el documento de paso para el CSV
        document = pd.read_csv(csv, header=None,sep=";", names=['nombre', 'apellido_paterno', 'apellido_materno', 'telefono', 'email'])
        #Para verificar la correcta llegada del CVS y su parametrización utilizar la linea de codigo siguiente en ambiente de depuración:
        print (document)
        #Se define variable para contador de correos enviados, se utiliza para serializar el asunto del mail
        numcorreo = 0
        email_from = settings.EMAIL_HOST_USER
        for j in document.index:
            numcorreo = numcorreo + 1
            nombre = document['nombre'][j]
            apellidop = document['apellido_paterno'][j]
            apellidom = document['apellido_materno'][j]
            fono = document['telefono'][j]
            mail_destinatario = document['email'][j]
            mensaje = 'Estimado Sr(a). ' + str(nombre) + ' ' + str(apellidop) + ' ' + str(apellidom) + ': Este correo es masivo'
            asunto = 'Correo Masivo N° ' + str(numcorreo)
            send_mail(
                asunto,
                mensaje,
                email_from,
                [mail_destinatario],
                fail_silently=False,
            )
            
        return render(request, "correomasivo.html")
    else:
            mensaje = "No se ha podido realizar el envio del email, intente nuevamente"
    return HttpResponse(mensaje)
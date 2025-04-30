# apps/integracion_dian/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SolicitudDescargaForm
from .models import SolicitudDescarga
import threading
import sys
import os

# Asegurar que se puede importar scripts.descargar_dian
from scripts.descargar_dian import ejecutar_con_token

def lanzar_proceso_dian(solicitud):
    try:
        solicitud.estado = "procesando"
        solicitud.save()
        ejecutar_con_token(solicitud.url_auth_token, solicitud.fecha_documentos)
        solicitud.estado = "completado"
        solicitud.save()
    except Exception as e:
        solicitud.estado = "error"
        solicitud.mensaje_error = str(e)
        solicitud.save()

@login_required
def crear_solicitud(request):
    if request.method == "POST":
        form = SolicitudDescargaForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user
            solicitud.save()
            threading.Thread(target=lanzar_proceso_dian, args=(solicitud,)).start()
            return redirect("solicitudes")
    else:
        form = SolicitudDescargaForm()
    return render(request, "integracion_dian/crear_solicitud.html", {"form": form})

# apps/integracion_dian/models.py
from django.db import models
from django.contrib.auth.models import User

class SolicitudDescarga(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    url_auth_token = models.TextField("URL del token de acceso de DIAN")
    fecha_documentos = models.DateField("Fecha de los documentos")
    creado_en = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[
        ("pendiente", "Pendiente"),
        ("procesando", "Procesando"),
        ("completado", "Completado"),
        ("error", "Error")
    ], default="pendiente")
    mensaje_error = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Solicitud #{self.id} - {self.usuario.username}"




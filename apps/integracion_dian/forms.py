# apps/integracion_dian/forms.py
from django import forms
from .models import SolicitudDescarga

class SolicitudDescargaForm(forms.ModelForm):
    class Meta:
        model = SolicitudDescarga
        fields = ["url_auth_token", "fecha_documentos"]
        widgets = {
            "fecha_documentos": forms.DateInput(attrs={"type": "date"}),
            "url_auth_token": forms.TextInput(attrs={"placeholder": "Pega aquí el enlace del correo DIAN"})
        }
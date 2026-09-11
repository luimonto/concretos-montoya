from django.shortcuts import render, get_object_or_404
from inventory.models import Asset

def detalle_maquina_qr(request, token):
    maquina = get_object_or_404(Asset, qr_token=token)
    
    return render(request, 'maquinas/detalle.html', {'maquina': maquina})

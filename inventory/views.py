from django.shortcuts import render, get_object_or_404

from inventory.models import Asset, AssetPhoto


def detalle_maquina_qr(request, token):
    maquina = get_object_or_404(
        Asset.objects.select_related(
            "category",
            "equipment_type",
            "brand",
        ).prefetch_related("photos"),
        qr_token=token,
    )

    foto_principal = maquina.photos.filter(
        photo_type=AssetPhoto.PhotoType.GENERAL
    ).first()

    return render(
        request,
        "maquinas/detalle.html",
        {
            "maquina": maquina,
            "foto_principal": foto_principal,
        },
    )
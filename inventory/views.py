from django.shortcuts import render, get_object_or_404
from inventory.models import Asset, AssetPhoto
from django.shortcuts import render


def index(request):
    return render(request, "index.html")


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

    last_movement = maquina.movements.all().order_by("-created_at").first()
    print(maquina)
    print()
    print(last_movement)
    print(last_movement.destination)

    return render(
        request,
        "maquinas/detalle.html",
        {
            "maquina": maquina,
            "foto_principal": foto_principal,
            "last_movement": last_movement,
        },
    )
from django.shortcuts import render, get_object_or_404, redirect
from inventory.models import Asset, AssetPhoto, Movement, Location
from accounts.models import EmployeeProfile
from project.models import Project


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

    return render(
        request,
        "maquinas/detalle.html",
        {
            "maquina": maquina,
            "foto_principal": foto_principal,
            "last_movement": last_movement,
        },
    )


def registrar_movimiento(request, token):
    maquina = get_object_or_404(
        Asset.objects.select_related(
            "category",
            "equipment_type",
            "brand",
        ),
        qr_token=token,
    )

    locations = Location.objects.filter(active=True).order_by("name")
    projects = Project.objects.all().order_by("name")
    employees = EmployeeProfile.objects.all().order_by("user__first_name")

    if request.method == "POST":
        movement_type = request.POST.get("movement_type")
        origin_id = request.POST.get("origin")
        destination_id = request.POST.get("destination")
        project_id = request.POST.get("project")
        responsible_id = request.POST.get("responsible")
        condition_out = request.POST.get("condition_out", "")
        condition_in = request.POST.get("condition_in", "")
        notes = request.POST.get("notes", "")

        print(movement_type, origin_id, destination_id, project_id, responsible_id, condition_out, condition_in, notes)
        Movement.objects.create(
            asset=maquina,
            movement_type=movement_type,
            origin_id=origin_id or None,
            destination_id=destination_id or None,
            project_id=project_id or None,
            responsible_id=responsible_id or None,
            condition_out=condition_out,
            condition_in=condition_in,
            notes=notes,
        )

        return redirect(
            "detalle_maquina_qr",
            token=maquina.qr_token,
        )

    return render(
        request,
        "maquinas/registrar_movimiento.html",
        {
            "maquina": maquina,
            "locations": locations,
            "projects": projects,
            "employees": employees,
            "movement_types": Movement.MovementType.choices,
            "conditions": Asset.PhysicalCondition.choices,
        },
    )
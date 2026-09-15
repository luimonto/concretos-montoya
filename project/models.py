from django.db import models
from inventory.models import Asset
from accounts.models import EmployeeProfile


class Project(models.Model):

    class Status(models.TextChoices):
        PLANNED = "planned", "Planeada"
        IN_PROGRESS = "in_progress", "En proceso"
        COMPLETED = "completed", "Terminada"
        CANCELLED = "cancelled", "Cancelada"

    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Código de obra",
        help_text="Ejemplo: OB-0001",
    )

    name = models.CharField(
        max_length=200,
        verbose_name="Nombre de la obra",
    )

    client = models.ForeignKey(
        "accounts.ClientProfile",
        on_delete=models.PROTECT,
        related_name="projects",
        verbose_name="Cliente"
    )

    address = models.TextField(
        blank=True,
        verbose_name="Dirección",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de inicio",
    )

    estimated_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha estimada de terminación",
    )

    actual_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha real de terminación",
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PLANNED,
        verbose_name="Estatus",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activa",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Observaciones",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Obra"
        verbose_name_plural = "Obras"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class ProjectAsset(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name="asset_assignments",
        verbose_name="Obra",
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name="project_assignments",
        verbose_name="Activo",
    )

    assigned_at = models.DateTimeField(
        verbose_name="Fecha de asignación",
    )

    returned_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de regreso",
    )

    condition_out = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Condición al salir",
    )

    condition_in = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Condición al regresar",
    )

    responsible = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.PROTECT,
        related_name="project_asset_assignments",
        null=True,
        blank=True,
        verbose_name="Responsable",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Observaciones",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Asignación de activo"
        verbose_name_plural = "Asignaciones de activos"
        ordering = ["-assigned_at"]

    def __str__(self):
        return f"{self.asset} → {self.project}"
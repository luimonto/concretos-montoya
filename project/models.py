from django.db import models
from django.db.models import Sum
from inventory.models import Asset
from accounts.models import EmployeeProfile

from decimal import Decimal


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

    progress = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Avance de obra (%)"
    )

    budget = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Presupuesto asignado"
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


class Product(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Producto",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    unit = models.CharField(
        max_length=50,
        verbose_name="Unidad",
        help_text="Ejemplo: pieza, bulto, kg, m3, litro",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["name"]


class Supplier(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Proveedor",
    )

    contact_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Contacto",
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Teléfono",
    )

    email = models.EmailField(
        blank=True,
        verbose_name="Correo",
    )

    tax_id = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="RFC",
    )

    address = models.TextField(
        blank=True,
        verbose_name="Dirección",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["name"]

class Requisition(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Borrador"
        PENDING = "pending", "Pendiente"
        APPROVED = "approved", "Aprobada"
        REJECTED = "rejected", "Rechazada"
        PURCHASED = "purchased", "Comprada"
        CANCELLED = "cancelled", "Cancelada"

    class Priority(models.TextChoices):
        LOW = "low", "Baja"
        NORMAL = "normal", "Normal"
        HIGH = "high", "Alta"
        URGENT = "urgent", "Urgente"

    project = models.ForeignKey(
        "Project",
        on_delete=models.PROTECT,
        related_name="requisitions",
        verbose_name="Obra",
    )

    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Código",
    )

    requested_by = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.PROTECT,
        related_name="requisitions",
        verbose_name="Solicitado por",
    )

    requested_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de solicitud",
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Estado",
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.NORMAL,
        verbose_name="Prioridad",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    estimated_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Total estimado",
        editable=False,
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Observaciones",
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de aprobación",
    )

    approved_by = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.PROTECT,
        related_name="approved_requisitions",
        null=True,
        blank=True,
        verbose_name="Aprobada por",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def recalculate_total(self):

        total = (
            self.items.aggregate(
                total=Sum("total")
            )["total"]
            or Decimal("0.00")
        )

        self.estimated_total = total

        Requisition.objects.filter(
            pk=self.pk
        ).update(
            estimated_total=total
        )

    def __str__(self):
        return f"{self.code} - {self.project}"

    class Meta:
        verbose_name = "Requisición"
        verbose_name_plural = "Requisiciones"
        ordering = ["-created_at"]


class RequisitionItem(models.Model):

    requisition = models.ForeignKey(
        Requisition,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Requisición",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="requisition_items",
        verbose_name="Producto",
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Descripción",
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Cantidad",
    )

    unit_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name="Precio unitario estimado",
    )

    total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Total",
        editable=False,
    )

    def save(self, *args, **kwargs):

        self.total = (
            self.quantity * self.unit_price
        )

        super().save(*args, **kwargs)

        self.requisition.recalculate_total()

    def delete(self, *args, **kwargs):
        requisition = self.requisition
        super().delete(*args, **kwargs)
        requisition.recalculate_total()

    def __str__(self):
        return f"{self.product} - {self.quantity}"

    class Meta:
        verbose_name = "Partida de requisición"
        verbose_name_plural = "Partidas de requisición"


class Expense(models.Model):

    class ExpenseType(models.TextChoices):
        MATERIAL = "material", "Material"
        SERVICE = "service", "Servicio"
        FUEL = "fuel", "Combustible"
        RENTAL = "rental", "Renta"
        TRANSPORT = "transport", "Transporte"
        OTHER = "other", "Otro"

    project = models.ForeignKey(
        "Project",
        on_delete=models.PROTECT,
        related_name="expenses",
        verbose_name="Obra",
    )

    requisition = models.ForeignKey(
        Requisition,
        on_delete=models.PROTECT,
        related_name="expenses",
        null=True,
        blank=True,
        verbose_name="Requisición",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="expenses",
        null=True,
        blank=True,
        verbose_name="Producto",
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="expenses",
        null=True,
        blank=True,
        verbose_name="Proveedor",
    )

    expense_type = models.CharField(
        max_length=30,
        choices=ExpenseType.choices,
        verbose_name="Tipo de gasto",
    )

    description = models.CharField(
        max_length=255,
        verbose_name="Descripción",
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=1,
        verbose_name="Cantidad",
    )

    unit_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name="Precio unitario",
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name="Importe",
    )

    invoice_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Factura / Ticket",
    )

    expense_date = models.DateField(
        verbose_name="Fecha del gasto",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Observaciones",
    )

    created_by = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.PROTECT,
        related_name="created_expenses",
        null=True,
        blank=True,
        verbose_name="Registrado por",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def save(self, *args, **kwargs):

        self.amount = (
            self.quantity * self.unit_price
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project} - ${self.amount}"

    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"
        ordering = ["-expense_date"]
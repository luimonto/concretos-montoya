import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings


class Brand(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    active = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activa",
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["name"]

    def __str__(self):
        return self.name


class EquipmentType(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="equipment_types",
        verbose_name="Categoría",
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Nombre",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    class Meta:
        verbose_name = "Tipo de equipo"
        verbose_name_plural = "Tipos de equipo"
        ordering = ["category", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"],
                name="unique_equipment_type_per_category",
            )
        ]

    def __str__(self):
        return f"{self.category} - {self.name}"


class Asset(models.Model):

    class IdentificationStatus(models.TextChoices):
        IDENTIFIED = "identified", "Identificado"
        PARTIAL = "partial", "Parcialmente identificado"
        PENDING = "pending", "Pendiente de identificación"
        DUPLICATE = "duplicate", "Duplicado por confirmar"

    class PhysicalCondition(models.TextChoices):
        NEW = "new", "Nuevo"
        GOOD = "good", "Bueno"
        REGULAR = "regular", "Regular"
        BAD = "bad", "Malo"
        REPAIR = "repair", "En reparación"
        OUT_OF_SERVICE = "out_of_service", "Fuera de servicio"

    asset_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="ID del activo",
    )

    qr_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="assets",
        verbose_name="Categoría",
    )

    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.PROTECT,
        related_name="assets",
        verbose_name="Tipo de equipo",
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="assets",
        verbose_name="Marca",
        blank=True,
    )

    model = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Modelo",
    )

    serial_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Número de serie",
    )

    engine_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Número de motor",
    )

    manufacturing_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Año de fabricación",
    )

    internal_inventory_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Número de inventario interno",
    )

    owner = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Propietario",
    )

    acquisition_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de adquisición",
    )

    physical_condition = models.CharField(
        max_length=30,
        choices=PhysicalCondition.choices,
        default=PhysicalCondition.REGULAR,
        verbose_name="Condición física",
    )

    identification_status = models.CharField(
        max_length=30,
        choices=IdentificationStatus.choices,
        default=IdentificationStatus.PENDING,
        verbose_name="Estatus de identificación",
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
        verbose_name = "Activo"
        verbose_name_plural = "Activos"
        ordering = ["asset_code"]

    def __str__(self):
        return f"{self.asset_code} - {self.brand} {self.model}"


@receiver(pre_save, sender=Asset)
def asset_code_autoincrement(sender, instance, **kwargs):
    if not instance.pk:
        last_asset_code = Asset.objects.all().order_by('created_at').last()
        if last_asset_code:
            prefix, code = last_asset_code.asset_code.split('-', 1)
            code = int(code) + 1
            instance.asset_code = f"{prefix}-{code:04d}"
        else:
            instance.asset_code = "CM-0001"


class Location(models.Model):

    class LocationType(models.TextChoices):
        WAREHOUSE = "warehouse", "Bodega"
        PROJECT = "project", "Obra"
        WORKSHOP = "workshop", "Taller"
        OTHER = "other", "Otro"

    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre",
    )

    location_type = models.CharField(
        max_length=30,
        choices=LocationType.choices,
        verbose_name="Tipo de ubicación",
    )

    address = models.TextField(
        blank=True,
        verbose_name="Dirección",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Observaciones",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activa",
    )

    def __str__(self):
        return self.name


class Movement(models.Model):

    from project.models import Project

    class MovementType(models.TextChoices):
        ENTRY = "entry", "Entrada"
        EXIT = "exit", "Salida"
        TRANSFER = "transfer", "Transferencia"
        RETURN = "return", "Regreso de obra"
        MAINTENANCE = "maintenance", "Envío a mantenimiento"

    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name="movements",
        verbose_name="Activo",
    )

    movement_type = models.CharField(
        max_length=30,
        choices=MovementType.choices,
        verbose_name="Tipo de movimiento",
    )

    movement_date = models.DateTimeField(
        verbose_name="Fecha y hora",
        auto_now_add=True
    )

    origin = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="movements_origin",
        null=True,
        blank=True,
        verbose_name="Ubicación origen",
    )

    destination = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="movements_destination",
        null=True,
        blank=True,
        verbose_name="Ubicación destino",
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name="movements",
        null=True,
        blank=True,
        verbose_name="Proyecto / Obra",
    )

    responsible = models.ForeignKey(
        "accounts.EmployeeProfile",
        on_delete=models.PROTECT,
        related_name="movements",
        null=True,
        blank=True,
        verbose_name="Responsable",
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

    return_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de regreso",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Observaciones",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"
        ordering = ["-movement_date"]

    def __str__(self):
        return f"{self.asset} - {self.get_movement_type_display()}"


class Document(models.Model):

    class DocumentType(models.TextChoices):
        INVOICE = "invoice", "Factura"
        OWNERSHIP = "ownership", "Documento de propiedad"
        PURCHASE = "purchase", "Comprobante de compra"
        IMPORT = "import", "Documento de importación"
        WARRANTY = "warranty", "Garantía"
        OTHER = "other", "Otro"

    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name="documents",
        verbose_name="Activo",
    )

    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices,
        verbose_name="Tipo de documento",
    )

    document_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Número de documento",
    )

    document_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha del documento",
    )

    file = models.FileField(
        upload_to="documents/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Archivo",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Observaciones",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.asset} - {self.get_document_type_display()}"


class AssetPhoto(models.Model):

    class PhotoType(models.TextChoices):
        GENERAL = "general", "Foto general"
        PLATE = "plate", "Placa de identificación"
        SERIAL = "serial", "Número de serie"
        ENGINE = "engine", "Motor"
        CONDITION = "condition", "Condición física"
        OTHER = "other", "Otra"

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="Activo",
    )

    photo_type = models.CharField(
        max_length=30,
        choices=PhotoType.choices,
        verbose_name="Tipo de fotografía",
    )

    image = models.ImageField(
        upload_to="assets/%Y/%m/",
        verbose_name="Fotografía",
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Descripción",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


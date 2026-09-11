import io
import base64
import qrcode
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Asset,
    AssetPhoto,
    Brand,
    Category,
    Document,
    EquipmentType,
    Location,
    Movement,
)


# ============================================================
# BRAND
# ============================================================

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "active",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


# ============================================================
# CATEGORY
# ============================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "active",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = (
        "name",
    )


# ============================================================
# EQUIPMENT TYPE
# ============================================================

@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "active",
    )

    list_filter = (
        "category",
        "active",
    )

    search_fields = (
        "name",
        "category__name",
        "description",
    )

    autocomplete_fields = (
        "category",
    )

    ordering = (
        "category",
        "name",
    )


# ============================================================
# ASSET PHOTOS INLINE
# ============================================================

class AssetPhotoInline(admin.TabularInline):
    model = AssetPhoto
    extra = 0

    fields = (
        "photo_type",
        "image",
        "description",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )


# ============================================================
# DOCUMENTS INLINE
# ============================================================

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0

    fields = (
        "document_type",
        "document_number",
        "document_date",
        "file",
        "notes",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )


# ============================================================
# MOVEMENTS INLINE
# ============================================================

class MovementInline(admin.TabularInline):
    model = Movement
    extra = 0

    fields = (
        "movement_type",
        "movement_date",
        "origin",
        "destination",
        "project",
        "responsible",
        "condition_out",
        "condition_in",
        "return_date",
        "notes",
    )

    readonly_fields = (
        "movement_date",
        "created_at",
    )

    ordering = (
        "-movement_date",
    )

    show_change_link = True


# ============================================================
# ASSET
# ============================================================
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):

    list_display = (
        "asset_code",
        "category",
        "equipment_type",
        "brand",
        "model",
        "serial_number",
        "physical_condition",
        "identification_status",
        "current_location_display",
        "qr_code_image",
    )

    list_filter = (
        "category",
        "equipment_type",
        "brand",
        "physical_condition",
        "identification_status",
        "manufacturing_year",
    )

    search_fields = (
        "asset_code",
        "category__name",
        "equipment_type__name",
        "brand__name",
        "model",
        "serial_number",
        "engine_number",
        "internal_inventory_number",
        "owner",
        "notes",
    )

    autocomplete_fields = (
        "category",
        "equipment_type",
        "brand",
    )

    readonly_fields = (
        "asset_code",
        "qr_token",
        "qr_code_image",
        "created_at",
        "updated_at",
        "current_location_display",
    )

    date_hierarchy = "created_at"

    ordering = (
        "asset_code",
    )

    fieldsets = (
        (
            "Identificación",
            {
                "fields": (
                    "category",
                    "equipment_type",
                    "brand",
                    "model",
                    "serial_number",
                    "engine_number",
                    "manufacturing_year",
                    "internal_inventory_number",
                ),
            },
        ),
        (
            "Propiedad y adquisición",
            {
                "fields": (
                    "owner",
                    "acquisition_date",
                ),
            },
        ),
        (
            "Estado",
            {
                "fields": (
                    "physical_condition",
                    "identification_status",
                    "current_location_display",
                ),
            },
        ),
        (
            "QR",
            {
                "fields": (
                    "qr_token",
                ),
                "description": (
                    "El QR se genera dinámicamente utilizando este identificador. "
                    "La imagen QR no se almacena en la base de datos."
                ),
            },
        ),
        (
            "Observaciones",
            {
                "fields": (
                    "notes",
                ),
            },
        ),
        (
            "Sistema",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
    )

    inlines = (
        MovementInline,
        DocumentInline,
        AssetPhotoInline,
    )

    def changelist_view(self, request, extra_context=None):
        self.current_request = request
        return super().changelist_view(request, extra_context=extra_context)

    def qr_code_image(self, obj):
        if not obj.qr_token:
            return "Sin QR"

        base_url = self.current_request.build_absolute_uri('/').rstrip('/')
        url = f"{base_url}/maquinas/info/{obj.qr_token}/"

        qr = qrcode.QRCode(
            version=1,
            box_size=4,
            border=2,
        )
        print(url)
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return format_html(
            '<a href="{}" target="_blank"><img src="data:image/png;base64,{}" style="max-height: auto; max-width: 200px;" /></a>',
            url,
            img_str,
        )

    def current_location_display(self, obj):
        """
        Obtiene la ubicación actual a partir del último movimiento
        registrado del activo.
        """
        movement = (
            obj.movements
            .select_related("destination")
            .order_by("-movement_date")
            .first()
        )

        if movement and movement.destination:
            return movement.destination.name

        return "Sin ubicación registrada"

    current_location_display.short_description = "Ubicación actual"
    qr_code_image.short_description = "Código QR"


# ============================================================
# LOCATION
# ============================================================

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "location_type",
        "active",
    )

    list_filter = (
        "location_type",
        "active",
    )

    search_fields = (
        "name",
        "address",
        "notes",
    )

    ordering = (
        "name",
    )


# ============================================================
# MOVEMENT
# ============================================================

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "movement_type",
        "movement_date",
        "origin",
        "destination",
        "project",
        "responsible",
    )

    list_filter = (
        "movement_type",
        "origin",
        "destination",
        "movement_date",
    )

    search_fields = (
        "asset__asset_code",
        "asset__serial_number",
        "asset__model",
        "project",
        "responsible",
        "notes",
    )

    autocomplete_fields = (
        "asset",
        "origin",
        "destination",
    )

    date_hierarchy = "movement_date"

    ordering = (
        "-movement_date",
    )

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Movimiento",
            {
                "fields": (
                    "asset",
                    "movement_type",
                    "movement_date",
                ),
            },
        ),
        (
            "Ubicación",
            {
                "fields": (
                    "origin",
                    "destination",
                    "project",
                ),
            },
        ),
        (
            "Responsabilidad",
            {
                "fields": (
                    "responsible",
                ),
            },
        ),
        (
            "Condición del equipo",
            {
                "fields": (
                    "condition_out",
                    "condition_in",
                    "return_date",
                ),
            },
        ),
        (
            "Observaciones",
            {
                "fields": (
                    "notes",
                ),
            },
        ),
        (
            "Sistema",
            {
                "fields": (
                    "created_at",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
    )


# ============================================================
# DOCUMENT
# ============================================================

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "document_type",
        "document_number",
        "document_date",
        "file_link",
        "created_at",
    )

    list_filter = (
        "document_type",
        "document_date",
    )

    search_fields = (
        "asset__asset_code",
        "asset__serial_number",
        "document_number",
        "notes",
    )

    autocomplete_fields = (
        "asset",
    )

    date_hierarchy = "document_date"

    ordering = (
        "-document_date",
    )

    readonly_fields = (
        "created_at",
    )

    def file_link(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">Ver archivo</a>',
                obj.file.url,
            )

        return "-"

    file_link.short_description = "Archivo"


# ============================================================
# ASSET PHOTO
# ============================================================

@admin.register(AssetPhoto)
class AssetPhotoAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "photo_type",
        "image_preview",
        "description",
        "created_at",
    )

    list_filter = (
        "photo_type",
        "created_at",
    )

    search_fields = (
        "asset__asset_code",
        "asset__serial_number",
        "description",
    )

    autocomplete_fields = (
        "asset",
    )

    readonly_fields = (
        "image_preview",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    fields = (
        "asset",
        "photo_type",
        "image",
        "image_preview",
        "description",
        "created_at",
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 250px;" />',
                obj.image.url,
            )

        return "Sin imagen"

    image_preview.short_description = "Vista previa"
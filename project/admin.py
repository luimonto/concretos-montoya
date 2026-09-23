from django.contrib import admin

from django.contrib import admin

from project.models import (
    Project,
    ProjectAsset,
    Product,
    Supplier,
    Requisition,
    RequisitionItem,
    Expense,
)


class ProjectAssetInline(admin.TabularInline):
    model = ProjectAsset
    extra = 0

    autocomplete_fields = ("asset",)

    fields = (
        "asset",
        "assigned_at",
        "returned_at",
        "responsible",
        "condition_out",
        "condition_in",
    )

    ordering = ("-assigned_at",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "client",
        "status",
        "start_date",
        "estimated_end_date",
        "active",
    )

    list_filter = (
        "status",
        "active",
    )

    search_fields = (
        "code",
        "name",
        "client__client_number",
        "client__business_name",
        "client__rfc",
    )

    inlines = (
        ProjectAssetInline,
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(ProjectAsset)
class ProjectAssetAdmin(admin.ModelAdmin):

    list_display = (
        "project",
        "asset",
        "assigned_at",
        "returned_at",
        "responsible",
        "condition_out",
        "condition_in",
    )

    list_filter = (
        "project",
        "condition_out",
        "condition_in",
    )

    search_fields = (
        "project__code",
        "project__name",
        "asset__asset_code",
        "asset__serial_number",
        "asset__model",
        "responsible",
    )

    autocomplete_fields = (
        "project",
        "asset",
    )

    date_hierarchy = "assigned_at"

    readonly_fields = (
        "created_at",
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "unit",
        "active",
        "created_at",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "name",
        "description",
    )

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "contact_name",
        "phone",
        "email",
        "tax_id",
        "active",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "name",
        "tax_id",
        "contact_name",
        "email",
    )

class RequisitionItemInline(admin.TabularInline):

    model = RequisitionItem

    extra = 1

    fields = (
        "product",
        "description",
        "quantity",
        "unit_price",
        "total",
    )

    readonly_fields = (
        "total",
    )

@admin.register(Requisition)
class RequisitionAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "project",
        "requested_by",
        "requested_at",
        "priority",
        "status",
        "estimated_total",
    )

    list_filter = (
        "status",
        "priority",
        "requested_at",
    )

    search_fields = (
        "code",
        "project__code",
        "project__name",
        "description",
    )

    readonly_fields = (
        "requested_at",
        "approved_at",
        "created_at",
        "updated_at",
    )

    inlines = [
        RequisitionItemInline,
    ]

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        "expense_date",
        "project",
        "expense_type",
        "product",
        "supplier",
        "description",
        "amount",
        "invoice_number",
    )

    list_filter = (
        "expense_type",
        "expense_date",
        "supplier",
        "project",
    )

    search_fields = (
        "description",
        "invoice_number",
        "project__code",
        "project__name",
        "supplier__name",
        "product__name",
    )

    readonly_fields = (
        "amount",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "project",
        "requisition",
        "product",
        "supplier",
    )
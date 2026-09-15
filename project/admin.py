from django.contrib import admin

from project.models import Project, ProjectAsset


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
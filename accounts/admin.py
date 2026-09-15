from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, EmployeeProfile, ClientProfile


# ============================================================
# USER
# ============================================================

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "user_type",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "user_type",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Información adicional",
            {
                "fields": (
                    "user_type",
                    "phone",
                    "active",
                ),
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Información adicional",
            {
                "fields": (
                    "user_type",
                    "phone",
                    "active",
                ),
            },
        ),
    )

    ordering = (
        "last_name",
        "first_name",
        "username",
    )


# ============================================================
# EMPLOYEE
# ============================================================

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):

    list_display = (
        "employee_number",
        "full_name",
        "position",
        "employment_status",
        "hire_date",
        "nss",
    )

    list_filter = (
        "position",
        "employment_status",
    )

    search_fields = (
        "employee_number",
        "nss",
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )

    autocomplete_fields = (
        "user",
    )

    fieldsets = (
        (
            "Información del empleado",
            {
                "fields": (
                    "employee_number",
                    "user",
                    "position",
                    "employment_status",
                ),
            },
        ),
        (
            "Información laboral",
            {
                "fields": (
                    "hire_date",
                    "termination_date",
                ),
            },
        ),
        (
            "Información de seguridad social",
            {
                "fields": (
                    "nss",
                ),
            },
        ),
        (
            "Información adicional",
            {
                "fields": (
                    "notes",
                ),
            },
        ),
        (
            "Auditoría",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    def full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    full_name.short_description = "Nombre"


# ============================================================
# CLIENT
# ============================================================

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):

    list_display = (
        "client_number",
        "business_name",
        "client_type",
        "rfc",
        "phone",
        "email",
        "active",
    )

    list_filter = (
        "client_type",
        "active",
    )

    search_fields = (
        "client_number",
        "rfc",
        "business_name",
        "phone",
        "email",
        "user__username",
        "user__first_name",
        "user__last_name",
    )

    autocomplete_fields = (
        "user",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Información del cliente",
            {
                "fields": (
                    "client_number",
                    "client_type",
                    "business_name",
                    "rfc",
                    "active",
                ),
            },
        ),
        (
            "Datos de contacto",
            {
                "fields": (
                    "phone",
                    "email",
                ),
            },
        ),
        (
            "Domicilio fiscal",
            {
                "fields": (
                    "tax_address",
                ),
            },
        ),
        (
            "Usuario del sistema",
            {
                "fields": (
                    "user",
                ),
            },
        ),
        (
            "Información adicional",
            {
                "fields": (
                    "notes",
                ),
            },
        ),
        (
            "Auditoría",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
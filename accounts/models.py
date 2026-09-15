
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class UserType(models.TextChoices):
        EMPLOYEE = "employee", "Empleado"
        CLIENT = "client", "Cliente"

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        verbose_name="Tipo de usuario",
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Teléfono",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.get_full_name() or self.username


class EmployeeProfile(models.Model):

    class EmploymentStatus(models.TextChoices):
        ACTIVE = "active", "Activo"
        INACTIVE = "inactive", "Inactivo"
        TERMINATED = "terminated", "Baja"

    class Position(models.TextChoices):
        ADMINISTRATIVE = "administrative", "Administrativo"
        FOREMAN = "foreman", "Maestro de obra"
        LABORER = "laborer", "Chalán"
        OPERATOR = "operator", "Operador"
        SUPERVISOR = "supervisor", "Supervisor"
        OTHER = "other", "Otro"

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="employee_profile",
        verbose_name="Usuario",
    )

    employee_number = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Número de empleado",
    )

    nss = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="NSS",
    )

    hire_date = models.DateField(
        verbose_name="Fecha de ingreso",
    )

    termination_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de baja",
    )

    position = models.CharField(
        max_length=30,
        choices=Position.choices,
        verbose_name="Puesto",
    )

    employment_status = models.CharField(
        max_length=20,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.ACTIVE,
        verbose_name="Estatus laboral",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Observaciones",
    )

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ["employee_number"]

    def __str__(self):
        return f"{self.employee_number} - {self.user.get_full_name()}"


class ClientProfile(models.Model):

    class ClientType(models.TextChoices):
        INDIVIDUAL = "individual", "Persona física"
        COMPANY = "company", "Persona moral"

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="client_profile",
        verbose_name="Usuario",
    )

    client_number = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Número de cliente",
    )

    client_type = models.CharField(
        max_length=20,
        choices=ClientType.choices,
        verbose_name="Tipo de cliente",
    )

    rfc = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="RFC",
    )

    business_name = models.CharField(
        max_length=250,
        verbose_name="Razón social / Nombre",
    )

    tax_address = models.TextField(
        blank=True,
        verbose_name="Domicilio fiscal",
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Teléfono",
    )

    email = models.EmailField(
        blank=True,
        verbose_name="Correo electrónico",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Observaciones",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["business_name"]

    def __str__(self):
        return f"{self.client_number} - {self.business_name}"
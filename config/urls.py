from django.contrib import admin
from django.urls import path
from inventory import views
from project import views as project_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path('maquinas/info/<str:token>/', views.detalle_maquina_qr, name='detalle_maquina_qr'),
    path(
        "maquinas/qr/<uuid:token>/movimiento/",
        views.registrar_movimiento,
        name="registrar_movimiento",
    ),
    path(
        "dashboard/",
        project_views.dashboard,
        name="project_dashboard",
    ),
]

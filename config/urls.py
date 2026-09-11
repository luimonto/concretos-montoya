from django.contrib import admin
from django.urls import path
from inventory import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('maquinas/info/<str:token>/', views.detalle_maquina_qr, name='detalle_maquina_qr'),
]

from django.urls import path, include
from .views import *
from proyecto_final.views import login_request
from django.conf import settings
from django.conf.urls.static import static

# app_name = 'ProductosApp'

urlpatterns = [
    path('proteinas/', proteins, name="productos_proteinas"),
    path('creatinas/', creatines, name="productos_creatinas"),
    path('otros/', otros, name="productos_otros"),
    path('todos/', todos, name="productos_todos"),
    path('detalle/<id>/', comentario, name="comentar_producto"),
    path('administrar/', administrar_productos, name="administrar_productos"),
    path('editarproducto/<id>', editar_producto, name="editar_producto"),
    path('eliminarproducto/<id>', eliminar_producto, name="eliminar_producto"),
    path('crearproducto/', crear_producto, name="crear_producto"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
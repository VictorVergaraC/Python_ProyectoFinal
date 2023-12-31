from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from ProductosApp.views import *
from CarritoApp.views import *
from CompraApp.views import *
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_productos, name="home_productos" ),
    path('pagina_no_disponible', no_disponible, name="no_disponible" ),
    path('acerca', acerca_de_mi, name="acerca_de" ),
    path('registrarme/', registrarme, name='registrarme'),
    path('login/', login_request, name="login" ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('usuario/misdatos/', mis_datos, name="mis_datos" ),
    path('usuario/miscompras/', mis_compras, name="mis_compras"),
    path('usuario/detallecompra/<id>', compra_detalle, name="detalle_compra"),
    

    path('productos/', include("ProductosApp.urls")),
    path('carrito/', include("CarritoApp.urls")),
    path('compras/', include("CompraApp.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

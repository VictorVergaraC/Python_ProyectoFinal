from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from ProductosApp.views import *
from CarritoApp.views import *
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_productos, name="home_productos" ),
    path('registrarme/', registrarme, name='registrarme'),
    path('login/', login_request, name="login" ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('usuario/misdatos/', mis_datos, name="mis_datos" ),
    path('usuario/miscompras/', mis_compras, name="mis_compras" ),

    path('productos/', include("ProductosApp.urls")),
    path('carrito/', include("CarritoApp.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

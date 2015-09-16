from django.conf.urls import patterns, include, url
from django.contrib import admin
from app_HOI import views
from . import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.inicio_sesion,name = 'inicio_sesion'),
    url(r'^registrar',views.registro,name = 'registrar'),
    url(r'^recuperarContraseña$', views.recuperarContraseña, name = 'recuperarContraseña'),
    url(r'^crearItem',views.crearItem,name = 'crearItem'),
    url(r'^categorias$',views.categoria,name = 'categoria'),
    url(r'^categorias/(?P<_id>\d+)/editar',views.categoria_editar,name = 'categoria_editar'),
    url(r'^inventario$',views.inventario,name = 'inventario'),
    url(r'^inventario/(?P<_id>\d+)/editar',views.item_editar,name = 'item_editar'),
    url(r'^verperfil$', views.verperfil, name = 'verperfil'),
    url(r'^perfil/(?P<_id>\d+)/editar', views.perfil_editar, name = 'perfil_editar'),
    url(r'^solicitud$', views.solicitud, name = 'solicitud'),
    url(r'^crearSolicitud',views.crearSolicitud,name = 'crearSolicitud'),
    url(r'^solicitud/(?P<_id>\d+)/eliminar', views.solicitud_eliminar,name = 'solicitud_eliminar'),
    url(r'^solicitud_estado/(?P<_id>\d+)/(?P<_nuevo_estado>[A|R]+)', views.solicitud_estado,name = 'solicitud_estado'),
    url(r'^inventario/(?P<_id>\d+)/ingresar', views.item_ingresar, name = 'item_ingresar'),
    url(r'^inventario/(?P<_id>\d+)/retirar', views.item_retirar, name = 'item_retirar'),    
    url(r'^cerrarSesion$', views.cerrarSesion, name = 'cerrarSesion'),
    url(r'^reporte$',views.imprimirReporte, name='reporte')

)

urlpatterns += patterns('', (
    r'^static/(?P<path>.*)$',
    'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT}
))

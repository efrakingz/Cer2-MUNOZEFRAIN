from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),  # Página principal
    path('login/', views.login_view, name='login'),  # Página de login
    path('registro/', views.register_view, name='registro'),  # Página de registro
    path('logout/', views.logout_view, name='logout'),  # Cerrar sesión
    path('agregar-carrito/<int:producto_id>/', views.agregar_carrito_view, name='agregar_carrito'),  # Agregar al carrito
    path('carrito/', views.carrito_view, name='carrito'),  # Ver carrito
    path('confirmar-pedido/', views.confirmar_pedido_view, name='confirmar_pedido'),
     path('eliminar-una-unidad/<int:item_id>/', views.eliminar_una_unidad_view, name='eliminar_una_unidad'),
    path('eliminar-carrito/<int:item_id>/', views.eliminar_carrito_view, name='eliminar_carrito'),  # Eliminar del carrito
]

from django.urls import path
from .views import detail, lista_productos

urlpatterns = [
    path('', lista_productos, name='lista_productos'),
    path('detail/<int:id>/', detail, name='detalle_producto'),
]
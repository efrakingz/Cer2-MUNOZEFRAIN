from django.db import models
from django.contrib.auth.models import User  # Si el carrito está relacionado con el usuario

# Modelo para Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')  # Si tienes imágenes de productos
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre

# Modelo para Carrito
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='ItemCarrito')  # Relación con Producto

    def __str__(self):
        return f"Carrito de {self.usuario}"

# Modelo intermedio para relacionar el carrito y los productos
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"


class CarritoItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.producto.nombre} - Cantidad: {self.cantidad}"
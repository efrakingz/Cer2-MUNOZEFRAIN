from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Producto, Carrito, ItemCarrito 
from django.shortcuts import redirect, get_object_or_404
from .models import CarritoItem  
from django.contrib.auth.models import User
from django.contrib import messages
# Vista para el inicio (index)
def index_view(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    return render(request, 'index.html', {'productos': productos})

# Vista para login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}, has iniciado sesión correctamente!')
                return redirect('index')  # Redirigir a la página principal
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Formulario inválido. Revisa los campos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vista para registro
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect('login')

    return render(request, 'registro.html')

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('index')

# Vista para agregar productos al carrito
def agregar_carrito_view(request, producto_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para agregar productos al carrito.')
        return redirect('login')
    
    producto = Producto.objects.get(id=producto_id)
    
    # Obtener o crear el carrito del usuario
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    # Buscar si ya existe un item del producto en el carrito
    item_carrito, item_created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)

    # Incrementar la cantidad si ya existe el item
    if not item_created:
        item_carrito.cantidad += 1
    item_carrito.save()
    
    messages.success(request, f'{producto.nombre} se ha agregado al carrito.')
    return redirect('index')

# Vista para ver el carrito de compras
def carrito_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para ver tu carrito.')
        return redirect('login')
    
    # Obtener todos los items del carrito para el usuario actual
    carrito_items = ItemCarrito.objects.filter(carrito__usuario=request.user)
    
    # Calcular el total del carrito
    total_carrito = sum(item.producto.precio * item.cantidad for item in carrito_items)
    
    return render(request, 'carrito.html', {'carrito': carrito_items, 'total_carrito': total_carrito})

# Vista para eliminar productos del carrito
def eliminar_carrito_view(request, item_id):
    item = ItemCarrito.objects.get(id=item_id, carrito__usuario=request.user)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('carrito')
def confirmar_pedido_view(request):
    # Lógica para confirmar el pedido (esto dependerá de lo que quieras hacer)
    carrito = Carrito.objects.filter(usuario=request.user)
    carrito.delete()


    return render(request, 'confirmar_pedido.html')

def eliminar_una_unidad_view(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)  # Asegúrate de usar ItemCarrito aquí

    # Reducir la cantidad en 1
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        # Si la cantidad es 1, eliminamos el producto del carrito
        item.delete()

    return redirect('carrito')

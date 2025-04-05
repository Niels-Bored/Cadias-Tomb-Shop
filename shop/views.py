from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Producto
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    productos = Producto.objects.all().order_by('-id')[:3]  # Últimos 3 productos
    return render(request, 'shop/index.html', {'productos': productos})

def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('cart')  # redirige a zona restringida para usuarios normales
        else:
            return render(request, 'shop/login.html', {'error': 'Credenciales incorrectas'})
 
    return render(request, 'shop/login.html')

def registro(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'shop/signup.html', {'error': 'Las contraseñas no coinciden'})

        if User.objects.filter(username=username).exists():
            return render(request, 'shop/signup.html', {'error': 'El usuario ya existe'})

        user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password1)
        return redirect('login')  # o loguear automáticamente
    
    return render(request, 'shop/signup.html')

def cart(request):
    return render(request, 'shop/cart.html')

def contact(request):
    return render(request, 'shop/contact.html')

@login_required
def checkout(request):
    return render(request, 'shop/checkout.html')

def contact(request):
    return render(request, 'shop/contact.html')

def about(request):
    return render(request, 'shop/about.html')

def blog(request):
    return render(request, 'shop/blog.html')

def shop(request):
    query = request.GET.get('q', '')  # Obtener el valor del input (o vacío si no hay)
    productos = Producto.objects.filter(nombre__icontains=query) if query else Producto.objects.all()
    
    return render(request, 'shop/shop.html', {'productos': productos, 'query': query})

def thankyou(request):
    return render(request, 'shop/thankyou.html')
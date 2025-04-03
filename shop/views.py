from django.shortcuts import render
from .models import Producto

# Create your views here.
def home(request):
    productos = Producto.objects.all().order_by('-id')[:3]  # Últimos 3 productos
    return render(request, 'index.html', {'productos': productos})

def cart(request):
    return render(request, 'cart.html')

def contact(request):
    return render(request, 'contact.html')

def checkout(request):
    return render(request, 'checkout.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')

def shop(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    return render(request, 'shop.html', {'productos': productos})

def thankyou(request):
    return render(request, 'thankyou.html')
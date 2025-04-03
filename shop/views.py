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
    query = request.GET.get('q', '')  # Obtener el valor del input (o vacío si no hay)
    productos = Producto.objects.filter(nombre__icontains=query) if query else Producto.objects.all()
    
    return render(request, 'shop.html', {'productos': productos, 'query': query})

def thankyou(request):
    return render(request, 'thankyou.html')
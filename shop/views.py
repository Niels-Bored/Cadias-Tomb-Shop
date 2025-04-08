from django.views import View
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Producto, Blog
from django.contrib import messages

class HomeView(View):
    def get(self, request):
        blogs = Blog.objects.all().order_by('-id')[:3]
        productos = Producto.objects.filter(stock__gt=0).order_by('-id')[:3]
        return render(request, 'shop/index.html', {'productos': productos, 'blogs': blogs})

class LoginView(View):
    def get(self, request):
        return render(request, 'shop/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('cart')
        else:
            return render(request, 'shop/login.html', {'error': 'Credenciales incorrectas'})

class SignupView(View):
    def get(self, request):
        return render(request, 'shop/signup.html')
    
    def post(self, request):
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

        user = User.objects.create_user(
            first_name=firstname, last_name=lastname,
            username=username, email=email, password=password1
        )
        return redirect('login')

class UserView(LoginRequiredMixin, View):
    login_url = 'login'  # Redirige si no está autenticado

    def get(self, request):
        return render(request, 'shop/user.html', {
            'user': request.user
        })

    def post(self, request):
        user = request.user

        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Verificar si las contraseñas coinciden (opcional cambiarla)
        if password1 and password2:
            if password1 != password2:
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, 'shop/update_profile.html', {'user': user})
            else:
                user.set_password(password1)  # Cambiar contraseña

        # Actualizar los demás campos
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('user')

class CartView(View):
    def get(self, request):
        return render(request, 'shop/cart.html', {'user_authenticated': request.user.is_authenticated})

class CheckoutView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        return render(request, 'shop/checkout.html')

class ContactView(TemplateView):
    template_name = 'shop/contact.html'

class AboutView(TemplateView):
    template_name = 'shop/about.html'

class ThankYouView(TemplateView):
    template_name = 'shop/thankyou.html'

class BlogListView(View):
    def get(self, request):
        blogs = Blog.objects.all().order_by('-id')[:20]
        return render(request, 'shop/blog.html', {'blogs': blogs})

class ShopView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            productos = Producto.objects.filter(nombre__icontains=query, stock__gt=0)
        else:
            productos = Producto.objects.filter(stock__gt=0)
        return render(request, 'shop/shop.html', {'productos': productos, 'query': query})


""" from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Producto
from .models import Blog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    blogs = Blog.objects.all().order_by('-id')[:3]
    productos = Producto.objects.filter(stock__gt=0).order_by('-id')[:3]
    
    return render(request, 'shop/index.html', {'productos': productos, 'blogs': blogs})


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
    return render(request, 'shop/cart.html', {'user_authenticated': request.user.is_authenticated})

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
    blogs = Blog.objects.all().order_by('-id')[:20]  # Últimos 18 blogs
    return render(request, 'shop/blog.html', {'blogs': blogs})

def shop(request):
    query = request.GET.get('q', '')
    
    if query:
        productos = Producto.objects.filter(nombre__icontains=query, stock__gt=0)
    else:
        productos = Producto.objects.filter(stock__gt=0)
    
    return render(request, 'shop/shop.html', {'productos': productos, 'query': query})


def thankyou(request):
    return render(request, 'shop/thankyou.html') """
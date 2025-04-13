from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, InvalidPage
from django.views.generic import TemplateView, ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404
from django.views import View

from .models import Producto, Blog, Tag

class HomeView(View):
    def get(self, request):
        tag_nombre = request.GET.get("tag")
        tags = Tag.objects.all()

        if tag_nombre:
            tag = get_object_or_404(Tag, nombre=tag_nombre)
            blogs = Blog.objects.filter(tags=tag).order_by("-id")
        else:
            blogs = Blog.objects.all().order_by("-id")[:3]

        productos = Producto.objects.filter(stock__gt=0).order_by("-id")[:3]
        return render(
            request, "shop/index.html", {
                "productos": productos, 
                "blogs": blogs,
                "tags": tags,
                "tag_seleccionado": tag_nombre}
        )


class LoginView(View):
    def get(self, request):
        return render(request, "shop/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("cart")
        else:
            return render(
                request, "shop/login.html", {"error": "Credenciales incorrectas"}
            )


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class SignUpView(View):
    def get(self, request):
        return render(request, "shop/signup.html")

    def post(self, request):
        firstname = request.POST["first_name"]
        lastname = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            return render(
                request, "shop/signup.html", {"error": "Las contraseñas no coinciden"}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request, "shop/signup.html", {"error": "El usuario ya existe"}
            )
        
        if User.objects.filter(email=email).exists():
            return render(
                request, "shop/signup.html", {"error": "El correo ya fue usado"}
            )

        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            password=password1,
        )
        return redirect("login")


class UserView(LoginRequiredMixin, View):
    login_url = "login"  # Redirige si no está autenticado

    def get(self, request):
        return render(request, "shop/user.html", {"user": request.user})

    def post(self, request):
        user = request.user

        firstname = request.POST["first_name"]
        lastname = request.POST["last_name"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # Verificar si las contraseñas coinciden (opcional cambiarla)
        if password1 and password2:
            if password1 != password2:
                messages.error(request, "Las contraseñas no coinciden.")
                return render(request, "shop/update_profile.html", {"user": user})
            else:
                user.set_password(password1)  # Cambiar contraseña

        # Actualizar los demás campos
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        messages.success(request, "Perfil actualizado correctamente.")
        return redirect("user")


class CartView(View):
    def get(self, request):
        return render(
            request,
            "shop/cart.html",
            {"user_authenticated": request.user.is_authenticated},
        )

class CheckoutView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        return render(request, "shop/checkout.html")


class ContactView(TemplateView):
    template_name = "shop/contact.html"


class AboutView(TemplateView):
    template_name = "shop/about.html"


class ThankYouView(TemplateView):
    template_name = "shop/thankyou.html"


class BlogListView(View):
    def get(self, request):
        tag_nombre = request.GET.get("tag")
        tags = Tag.objects.all()

        if tag_nombre:
            tag = get_object_or_404(Tag, nombre=tag_nombre)
            blogs = Blog.objects.filter(tags=tag).order_by("-id")
        else:
            blogs = Blog.objects.all().order_by("-id")[:20]

        return render(request, "shop/blog.html", {
            "blogs": blogs,
            "tags": tags,
            "tag_seleccionado": tag_nombre
        })

class ShopView(View):
    def get(self, request, page=1):
        query = request.GET.get("q", "")
        
        if query:
            productos_queryset = Producto.objects.filter(nombre__icontains=query, stock__gt=0).order_by('-id')
        else:
            productos_queryset = Producto.objects.filter(stock__gt=0).order_by('-id')

        paginator = Paginator(productos_queryset, 20)

        try:
            productos = paginator.page(page)
        except InvalidPage:
            raise Http404("Página no válida")

        context = {
            "productos": productos,
            "query": query,
        }

        return render(request, "shop/shop.html", context)
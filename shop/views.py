from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, InvalidPage
from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.http import Http404
from django.views import View
from shop import decorators

from utils.stripe import get_stripe_link, update_transaction_link
from utils.emails import send_email
from utils import emails, tokens

from .models import Producto, Blog, Tag, Venta
from django.contrib.auth.models import User

import json

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

        message_title = "Excelente"
        message_text = "Tu usuario se ha creado correctamente. " \
            "Revisa tu correo para confirmar tu cuenta."
        message_type = "success"

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
            is_active=False
        )

        id_token = tokens.get_id_token(user)
       
        emails.send_email(
            subject="Activa tu cuenta",
            first_name=firstname,
            last_name=lastname,
            texts=[
                "¡Gracias por crear una cuenta!",
                "Tu cuenta se ha creado correctamente",
                "Sólo un paso más para empezar a usarla",
            ],
            cta_link=f"{settings.HOST}/activate/{id_token}/",
            cta_text="Activar cuenta",
            to_email=email,
        )

        return render(request, 'shop/signup.html', context={
            "title": "Sign Up",
            "message_title": message_title,
            "message_text": message_text,
            "message_type": message_type,
        })

class ActivationView(View):
    @method_decorator(decorators.logged(redirect_url='/'))
    def get(self, request, user_id: int, token: str):
        
        user = User.objects.filter(id=user_id)
        
        error_context = {
            "message_title": "Error de Activación",
            "message_text": "Revisa el enlace o intenta registrarte de nuevo",
            "message_type": "error"
        }
        error_response = render(request, 'shop/index.html', context=error_context)
        
        is_valid, user = tokens.validate_user_token(user_id, token, filter_active=False)
        
        # render error message if token is invalid
        if not is_valid:
            return error_response
        
        # Activate user
        user.is_active = True
        user.save()
        
        # Success message
        return render(request, 'shop/index.html', context={
            "message_title": "Cuenta activada",
            "message_text": "Tu cuenta ha sido activada correctamente. "
                            "Ahora puedes iniciar sesión",
            "message_type": "success"
        })
    
    
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

class CheckoutView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        return render(request, "shop/checkout.html")


class ContactView(TemplateView):
    def get(self, request):
        return render(request, "shop/contact.html")

    def post(self, request):
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        message = request.POST["message"]

        emails.send_email(
            subject=f"Tienes un nuevo mensaje en Cadia's Tomb Shop",
            first_name=firstname,
            last_name=lastname,
            texts=[
                f"Tienes un mensaje de {firstname} {lastname}",
                f"Mensaje: {message}",
                f"Correo de {firstname} {lastname}: {email}",
            ],
            cta_link=f"{settings.HOST}/admin/auth/user/",
            cta_text="Ir al panel de administración",
            to_email="abelsv168@gmail.com",
        )
        
        return render(request, 'shop/contact.html', context={
            "message_title": "Correo enviado",
            "message_text": "Tu correo ha sido enviado a los administradores. "
                            "Te responderemos en menos de 24 horas",
            "message_type": "success"
        })

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


class CartView(View):
    def get(self, request):
        return render(
            request,
            "shop/cart.html",
            {"user_authenticated": request.user.is_authenticated},
        )


class Sale(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"login_required": True})
       
        try:
            data = json.loads(request.body)
            username = data.get("username")
            productos = data.get("productos")
            datos_direccion = data.get("direccion")
        except:
            return JsonResponse({
                "status":"error",
                "message":"Invalid JSON",
                "data":{}
            })

        print(datos_direccion)
        print(datos_direccion["address"])
        productos_insuficientes = []

        description = ""
        total = 0
        products = []
        for item in productos:
            try:
                producto = Producto.objects.get(id=item["id"])
                if producto.stock < item["cantidad"]:
                    productos_insuficientes.append(item["id"])
            except Producto.DoesNotExist:
                productos_insuficientes.append(item["id"])
            else:
                description += f"{item['nombre']} x {item['cantidad']}\n"
                total+=float(item['precio'])*item["cantidad"]
                products.append(producto)

        if productos_insuficientes:
            return JsonResponse({
                "status":"error",
                "message":"Not enough stock",
                "data":{
                    "productos_insuficientes": productos_insuficientes
                }
            })
        
        users = User.objects.filter(username=username)
        if not users:
            return JsonResponse({
                "status":"error",
                "message":"Invalid username",
                "data":{}
            })

        user = users.first()

        if not datos_direccion["email"]:
            datos_direccion["email"] = user.email
        if not datos_direccion["phone"]:
            datos_direccion["phone"] = "No especificado"

        sale = Venta.objects.create(
            usuario=user, 
            direccion=datos_direccion["address"],
            tipo=datos_direccion["kind"],
            estado=datos_direccion["state"],
            codigo_postal=datos_direccion["postal_zip"],
            correo=datos_direccion["email"],
            telefono=datos_direccion["phone"],
            total=total,
            status="Pendiente")
        
        for item in productos:
            producto = Producto.objects.get(id=item["id"])
            sale.productos.add(producto)

        sale.save()

        stripe_url= get_stripe_link(
            product_name="Pedido",
            total=total,
            description=description, 
            email="abelsotovaldez@gmail.com", 
            sale_id=sale.id, 
            back_page="/cart" 
        )
        
        return JsonResponse({
                "status":"success",
                "message":"Compra realizada exitosamente",
                "data":{
                    "stripe_url":stripe_url
                }
            })
    
class SaleDoneView(View):
    def get(self, request, sale_id: str):
        """ Update sale status and redirect to landing

        Args:
            request (HttpRequest): Django request object
            sale_id (str): sale id from url
        """

        landing_done_page = settings.HOST
        landing_error_page = landing_done_page + f"?sale-id={sale_id}&sale-status=error"

        # Get sale
        sale = Venta.objects.filter(id=sale_id).first()
        if not sale:
            return redirect(landing_error_page)

        # Get link from stripe
        sale.save()
        
        # Update stock
        """ current_stock = models.StoreStatus.objects.get(key='current_stock')
        current_stock_int = int(current_stock.value)
        current_stock.value = str(current_stock_int - 1)
        current_stock.save() """

        # Get sale data
        sale_data = sale.get_sale_data_dict()

        email_texts = [
            "Your payment has been confirmed!",
            "Your order is being processed.",
            "You will receive notifications about the status of your order.",
            "Here your order details:"
        ]

        logo_url = ""

        # Confirmation email after payment
        send_email(
            subject="Nyx Trackers Payment Confirmation",
            first_name=sale.usuario.first_name,
            last_name=sale.usuario.last_name,
            texts=email_texts,
            cta_link=f"{settings.HOST}/admin/",
            cta_text="Go to dashboard",
            to_email=sale.usuario.email,
            key_items=sale_data,
            image_src=logo_url
        )

        # Send email to admin
        send_email(
            subject="Nyx Trackers New Sale",
            first_name="Admin",
            last_name="",
            texts=["A new sale has been made."],
            cta_link=f"{settings.HOST}/admin/store/sale/{sale_id}/change/",
            cta_text="View sale in dashboard",
            to_email=settings.ADMIN_EMAIL,
            key_items=sale_data,
            image_src=logo_url
        )

        landing_done_page += f"?sale-id={sale_id}&sale-status=success"
        return redirect(landing_done_page)

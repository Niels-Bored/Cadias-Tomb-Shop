from django.urls import path
from shop.views import HomeView, LoginView, SignupView, CartView, CheckoutView, ContactView, AboutView, ThankYouView, BlogListView, ShopView
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name='about'),
    path('thankyou/', ThankYouView.as_view(), name='thankyou'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('logout/', logout_view, name='logout')
]


""" from django.contrib import admin
from django.urls import path
from shop.views import home
from shop.views import inicio_sesion
from shop.views import registro
from shop.views import cart
from shop.views import about
from shop.views import checkout
from shop.views import contact
from shop.views import blog
from shop.views import shop
from shop.views import thankyou

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home, name='home'),
    path('login', inicio_sesion, name='login'),
    path('signup', registro, name='signup'),
    path('cart/', cart, name='cart'),
    path('about/', about, name='about'),
    path('checkout/', checkout, name='checkout'),
    path('contact/', contact, name='contact'),
    path('blog/', blog, name='blog'),
    path('shop/', shop, name='shop'),
    path('thankyou/', thankyou, name='thankyou'),
    path('logout/', logout_view, name='logout'),
]
 """
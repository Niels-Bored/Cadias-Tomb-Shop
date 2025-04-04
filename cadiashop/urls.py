"""
URL configuration for cadiashop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
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
]

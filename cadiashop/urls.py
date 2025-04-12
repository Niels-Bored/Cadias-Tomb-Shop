from django.urls import path
from django.contrib import admin
from shop.views import (
    HomeView,
    LoginView,
    LogoutView,
    SignUpView,
    UserView,
    CartView,
    CheckoutView,
    ContactView,
    AboutView,
    ThankYouView,
    BlogListView,
    ShopView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("user/", UserView.as_view(), name="user"),
    path("cart/", CartView.as_view(), name="cart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("about/", AboutView.as_view(), name="about"),
    path("thankyou/", ThankYouView.as_view(), name="thankyou"),
    path("blog/", BlogListView.as_view(), name="blog"),
    path("shop/", ShopView.as_view(), name="shop"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

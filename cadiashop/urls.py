from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

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
    ActivationView,
    SaleDoneView,
    Sale
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
    path('shop/<int:page>/', ShopView.as_view(), name='shop'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("activate/<int:user_id>-<token>/", ActivationView.as_view(), name='activate'),
    path('sale/', Sale.as_view(), name='sale'),
    path('sale-done/<sale_id>/', SaleDoneView.as_view(), name='sale-done')
]

if not settings.STORAGE_AWS:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
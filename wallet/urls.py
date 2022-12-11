from django.urls import path, include
from rest_framework import routers

from .views import WalletViewSet

router = routers.DefaultRouter()
router.register("wallets", WalletViewSet)


urlpatterns = [
    path("", include(router.urls)),
]


app_name = "wallet"

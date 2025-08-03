from django.urls import path

from wallet.apps import WalletConfig

from .views import OperationViewSet, WalletViewSet

app_name = WalletConfig.name

urlpatterns = [
    # path(
    #     "api/v1/wallets/create/",
    #     WalletViewSet.as_view({"post": "create"}),
    #     name="wallet-create",
    # ),
    # path("api/v1/wallets/", WalletViewSet.as_view({"get": "list"}), name="wallet-list"),
    path(
        "api/v1/wallets/<uuid:id>/",
        WalletViewSet.as_view({"get": "retrieve"}),
        name="wallet-detail",
    ),
    path(
        "api/v1/wallets/<uuid:id>/operation/",
        OperationViewSet.as_view({"post": "create"}),
        name="operation-create",
    ),
]

from rest_framework import serializers, viewsets

from .models import Operation, Wallet
from .serializers import OperationSerializer, WalletSerializer


class WalletViewSet(viewsets.ModelViewSet):
    """
    ViewSet для кошелька.
    """

    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    lookup_field = "id"


class OperationViewSet(viewsets.ModelViewSet):
    """
    ViewSet для операций кошелька.
    """

    serializer_class = OperationSerializer
    queryset = Operation.objects.all()

    def perform_create(self, serializer):
        wallet_id = self.kwargs.get("id")
        try:
            wallet = Wallet.objects.get(id=wallet_id)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError({"detail": "Кошелек не найден"})

        serializer.save(wallet=wallet)

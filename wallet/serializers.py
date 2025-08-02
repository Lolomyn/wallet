from rest_framework import serializers

from .models import Operation, Wallet


class WalletSerializer(serializers.ModelSerializer):
    """Сериализатор кошелька."""

    class Meta:
        model = Wallet
        fields = "__all__"


class OperationSerializer(serializers.ModelSerializer):
    """Сериализатор операции кошелька."""

    class Meta:
        model = Operation
        fields = ("operation_type", "amount")

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть положительной")
        return value

    def validate(self, data):
        wallet_id = self.context["view"].kwargs.get("id")
        if not wallet_id:
            raise serializers.ValidationError({"detail": "Не указан кошелек"})

        try:
            wallet = Wallet.objects.get(id=wallet_id)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError({"detail": "Кошелек не найден"})

        if (
            data["operation_type"] == Operation.WITHDRAW
            and wallet.balance < data["amount"]
        ):
            raise serializers.ValidationError(
                {"detail": "Недостаточно средств на кошельке"}
            )

        return data

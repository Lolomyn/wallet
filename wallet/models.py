import uuid
from django.db import models
from django.db import transaction
from django.db.models import F


class Wallet(models.Model):
    """Модель Кошелька"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Баланс кошелька"
    )

    def __str__(self):
        return f"UUID: {self.id} - balance: {self.balance}"

    class Meta:
        verbose_name = "Кошелек"
        verbose_name_plural = "Кошельки"


class Operation(models.Model):
    """Модель операций над кошельком"""

    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"

    OPERATION_CHOICES = [(DEPOSIT, "DEPOSIT"), (WITHDRAW, "WITHDRAW")]

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="operations",
        verbose_name="Кошелек",
    )

    operation_type = models.CharField(
        max_length=8,
        choices=OPERATION_CHOICES,
        default=WITHDRAW,
        verbose_name="Тип операции",
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма")

    def __str__(self):
        return f"Operation: {self.operation_type} - amount: {self.amount}"

    def save(self, *args, **kwargs):
        # Применяем изменение баланса только при создании операции
        is_creating = self._state.adding
        if is_creating:
            with transaction.atomic():
                # Блокируем строку кошелька для корректной конкуррентной работы
                locked_wallet = Wallet.objects.select_for_update().get(pk=self.wallet_id)

                if self.operation_type == self.DEPOSIT:
                    Wallet.objects.filter(pk=locked_wallet.pk).update(
                        balance=F("balance") + self.amount
                    )
                elif self.operation_type == self.WITHDRAW:
                    if locked_wallet.balance < self.amount:
                        raise ValueError("Недостаточно средств")
                    Wallet.objects.filter(pk=locked_wallet.pk).update(
                        balance=F("balance") - self.amount
                    )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"

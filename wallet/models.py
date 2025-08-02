import uuid

from django.db import models


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
        if self.operation_type == self.DEPOSIT:
            self.wallet.balance += self.amount

        elif self.operation_type == self.WITHDRAW:
            if self.wallet.balance < self.amount:
                raise ValueError("Недостаточно средств")
            self.wallet.balance -= self.amount

        self.wallet.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"

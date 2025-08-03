from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from wallet.models import Operation, Wallet


class WalletTestCase(APITestCase):
    """Тестирование эндпоинта получения баланса кошелька"""

    def setUp(self) -> None:
        self.wallet = Wallet.objects.create(balance=2500)
        self.wrong_wallet_uuid = "12345678-1234-1234-1234-123456789012"

    def test_get_wallet_balance(self):
        """Тестирование корректной работы получения баланса кошелька"""
        response = self.client.get(f"/api/v1/wallets/{self.wallet.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data["balance"]), 2500.00)

    def test_get_non_existent_wallet_balance(self):
        """Тестирование ошибочно введенного uuid кошелька"""
        response = self.client.get(f"/api/v1/wallets/{self.wrong_wallet_uuid}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "No Wallet matches the given query.")


class OperationTestCase(APITestCase):
    """Тестирование эндпоинта операции по кошельку"""

    def setUp(self) -> None:
        self.wallet = Wallet.objects.create(balance=2500)
        self.deposit_data = {"operation_type": "deposit", "amount": 1000.00}
        self.withdraw_data = {"operation_type": "withdraw", "amount": 1000.00}

        self.withdraw_data_a_lot = {"operation_type": "withdraw", "amount": 10000.00}
        self.wrong_wallet_uuid = "12345678-1234-1234-1234-123456789012"

    def test_create_deposit_operation(self):
        response = self.client.post(
            f"/api/v1/wallets/{self.wallet.id}/operation/", data=self.deposit_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(f"/api/v1/wallets/{self.wallet.id}/")
        self.assertEqual(float(response.data["balance"]), 3500.00)

    def test_create_withdraw_operation(self):
        response = self.client.post(
            f"/api/v1/wallets/{self.wallet.id}/operation/", data=self.withdraw_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(f"/api/v1/wallets/{self.wallet.id}/")
        self.assertEqual(float(response.data["balance"]), 1500.00)

    def test_create_withdraw_operation_with_insufficient_funds(self):
        response = self.client.post(
            f"/api/v1/wallets/{self.wallet.id}/operation/",
            data=self.withdraw_data_a_lot,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"][0], "Недостаточно средств на кошельке")

    def test_create_operation_with_incorrect_wallet(self):
        response = self.client.post(
            f"/api/v1/wallets/{self.wrong_wallet_uuid}/operation/",
            data=self.deposit_data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"][0], "Кошелек не найден")

    def test_create_operation_with_negative_amount(self):
        data = {"operation_type": "withdraw", "amount": -2000}

        response = self.client.post(
            f"/api/v1/wallets/{self.wallet.id}/operation/",
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["amount"][0], "Сумма должна быть положительной")

    def test_create_operation_with_incorrect_amount(self):
        data = {"operation_type": "withdraw", "amount": "something wrong"}

        response = self.client.post(
            f"/api/v1/wallets/{self.wallet.id}/operation/",
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["amount"][0], "Требуется численное значение.")

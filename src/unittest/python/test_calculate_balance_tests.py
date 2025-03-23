import unittest
import hashlib
import sys
import os
from freezegun import freeze_time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../main/python")))
from uc3m_money.account_deposit import AccountDeposit
from uc3m_money.json_manager import JsonManager
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_manager import AccountManager


# Datos de prueba para simular el JSON de entrada
transactions_file = "RF3/transactions.json"
balance_file = "RF3/saldos.json"

freeze_date = "2024-03-22 10:00:00"

class TestAccountManager(unittest.TestCase):
    """Class for testing the AccountDeposit class"""

    @freeze_time(freeze_date)
    def test_valid_tc1(self):
        """Test for the deposit_request method"""
        AccountManager().calculate_balance("ES8658342044541216872704")


    def test_invalid_tc1(self):

        with self.assertRaises(AccountManagementException) as cm:
            AccountManager().calculate_balance("ES865844541216872704")

        self.assertEqual(str(cm.exception), "Excepción: La cadena de entrada no contiene un IBAN válido.")

"""
        data = JsonManager(balance_file).read_json()
        balance = AccountManager.balance_esperado("ES8658342044541216872704")
        self.assertEqual(data[0]["SALDO"], balance)
"""
if __name__ == "__main__":
    unittest.main()

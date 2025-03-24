"""Tests for the calculate_balance method in the AccountManager class"""
import unittest
import sys
import os
from freezegun import freeze_time
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_manager import AccountManager

# Añadimos el path para poder importar los módulos necesarios
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../main/python")))
# Fecha de congelación para los tests
FREEZE_DATE = "2024-03-22 10:00:00"

class TestAccountManager(unittest.TestCase):
    """Class for testing the AccountDeposit class"""

    @freeze_time(FREEZE_DATE)
    def test_valid_tc1(self):
        """Test for the deposit_request method"""
        AccountManager().calculate_balance("ES8658342044541216872704")

    @freeze_time(FREEZE_DATE)
    def test_invalid_tc1(self):
        """Test with empty JSON object"""
        with self.assertRaises(AccountManagementException) as cm:
            AccountManager().calculate_balance("ES865844541216872704")
        self.assertEqual(str(cm.exception),
                         "Excepción: La cadena de entrada no contiene un IBAN válido.")


if __name__ == "__main__":
    unittest.main()

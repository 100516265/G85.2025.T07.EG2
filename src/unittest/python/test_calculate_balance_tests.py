"""Tests for the calculate_balance method in the AccountManager class"""
import unittest
import sys
import os
from unittest.mock import patch
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
        resultado = AccountManager.calculate_balance("ES8658342044541216872704")
        self.assertEqual(resultado, True)


    @freeze_time(FREEZE_DATE)
    def test_invalid_tc1(self):
        """Test with an invalid IBAN"""
        with self.assertRaises(AccountManagementException) as cm:
            AccountManager.calculate_balance("ES865844541216872704")

        self.assertEqual(str(cm.exception),
                         "Excepción: La cadena de entrada no contiene un IBAN válido.")

    @freeze_time(FREEZE_DATE)
    @patch("uc3m_money.json_manager.JsonManager.read_json", return_value=None)
    def test_invalid_tc2(self, _mock_read_json):
        """Test when JSON object does not exist"""
        with self.assertRaises(AccountManagementException) as cm:
            AccountManager.calculate_balance("ES8658342044541216872704")

        self.assertEqual(str(cm.exception),
                         "Excepción:Error de procesamiento interno al procesar el código")

    @freeze_time(FREEZE_DATE)
    @patch("uc3m_money.json_manager.JsonManager.read_json", return_value=[{
        "IBAN": "ES8658342044541216872704",
        "amount": "+2424.42"
    }])
    def test_invalid_tc3(self, _mock_read_json):
        """Test when IBAN not found"""
        with self.assertRaises(AccountManagementException) as cm:
            AccountManager.calculate_balance("ES4500817294770123456789")

        self.assertEqual(str(cm.exception),
                         "Excepción: El IBAN no se encuentra en el fichero de movimientos")



    @freeze_time(FREEZE_DATE)
    @patch("uc3m_money.json_manager.JsonManager.read_json", return_value=[{}])
    def test_invalid_tc4(self, _mock_read_json):
        """Test with empty JSON object"""
        with self.assertRaises(AccountManagementException) as cm:
            AccountManager.calculate_balance("ES8658342044541216872704")

        self.assertEqual(str(cm.exception),
                         "Excepción: El IBAN no se encuentra en el fichero de movimientos")



    @freeze_time(FREEZE_DATE)
    @patch("uc3m_money.json_manager.JsonManager.read_json", return_value= [{
        "IBAN": "ES8658342044541216872704",
        "amount": "+2424.42"
    },
    {
        "IBAN": "ES3559005439021242088295",
        "amount": "+1258.75"
    }])
    def test_valid_tc2(self, _mock_read_json):
        """Test entra dos veces"""
        resultado = AccountManager.calculate_balance("ES3559005439021242088295")
        self.assertEqual(resultado, True)




if __name__ == "__main__":
    unittest.main()

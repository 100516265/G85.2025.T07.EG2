import unittest
import hashlib
import sys
import os
from freezegun import freeze_time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../main/python")))
from uc3m_money.account_manager import AccountManager
from uc3m_money.account_deposit import AccountDeposit
from uc3m_money.json_manager import JsonManager

# Datos de prueba para simular el JSON de entrada
input_file = "RF2/deposit_requests.json"
storage_file = "RF2/deposit_store.json"

class TestAccountDeposit(unittest.TestCase):
    """Class for testing the AccountDeposit class"""

    @freeze_time("2026-02-02 00:00:00")
    def test_deposit_request(self):
        """Test for the deposit_request method"""
        # Crear objeto AccountDeposit
        to_iban_to_test = "ES4500817294770123456789"
        deposit_amount_to_test = 250.50
        deposit = AccountDeposit(to_iban=to_iban_to_test, deposit_amount=deposit_amount_to_test)

        result = deposit.deposit_request(input_file=input_file, storage_file=storage_file)

        # Verificar la firma generada
        expected_signature = hashlib.sha256(
            "{alg:SHA-256,typ:DEPOSIT,iban:ES4500817294770123456789,amount:100.0,deposit_date:1765075200.0}".encode()
        ).hexdigest()

        self.assertEqual(result, expected_signature)


if __name__ == "__main__":
    unittest.main()

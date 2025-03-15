"""class for testing the register_order method"""
import unittest
import sys
import os
from freezegun import freeze_time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../main/python")))
from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_manager import AccountManager
from uc3m_money.account_management_exception import AccountManagementException

freeze_date = "2025-03-22 10:00:00"


class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""
    global freeze_date
    """Tests for the AccountManager's transfer request"""

    @freeze_time(freeze_date)
    def test_valid_TC1(self):
        """Valid transfer request"""
        my_manager = AccountManager()
        from_iban_to_test = "ES60636390983922098113875"
        to_iban_to_test = "ES60636390983922098113875"
        concept_to_test = "transfer for rent"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
        type_to_test = "URGENT"
        with freeze_time(freeze_date):
            result = my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

if __name__ == '__main__':
    unittest.main()



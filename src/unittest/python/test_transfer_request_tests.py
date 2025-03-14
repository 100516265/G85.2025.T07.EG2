"""class for testing the register_order method"""
import unittest
from uc3m_money import AccountManager
from uc3m_money import AccountManagementException

class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""
    def test_valid_TC1( self ):
        my_manager = AccountManager()
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test="ES4500817294770123456789"
        concept_to_test= "text valid"
        amount_to_test = "10.00"
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        result = my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                             transfer_concept=concept_to_test, transfer_type=type_to_test,
                                             transfer_date=date_to_test, transfer_amount=amount_to_test)

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()

"""Module
from .account_management_exception import AccountManagementException
from .transfer_request import TransferRequest
"""

class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_iban(iban: str) ->bool:
        """
        Validates whether a given IBAN is correctly formatted
        and has valid control digits
        :param iban: The IBAN to validate
        :return: True if the IBAN is valid
        """

        if(not isinstance(iban, str)
            or not iban.startswith("ES")
            or len(iban)!=24
            or not iban[2:].isdigit()):
            return False

        control_digits = int(iban[2:4])
        iban_number = int(iban[4:] + "142800") % 97
        calculated_control_digits = 98 - iban_number

        return control_digits == calculated_control_digits


    @staticmethod
    def validate_concept(concept: str) ->bool:

        if(not isinstance(concept, str)
            or not (10<= len(concept) <= 30)):
            return False


    @staticmethod
    def validate_type(type: str) ->bool:

        if not isinstance(type, str):
            return False
        if type == "ORDINARY" or "URGENT" or "INMEDIATE":
            return True

    @staticmethod
    def validate_date(date: str) -> bool:

        if not isinstance(date, str):
            return False

    @staticmethod
    def validate_amount(amount: str) -> bool:

        if (not isinstance(amount, float))\
            or not (10.00 <= amount <= 10000.00):
            return False

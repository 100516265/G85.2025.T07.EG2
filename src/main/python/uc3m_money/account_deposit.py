"""Contains the class OrderShipping"""
import hashlib
from datetime import datetime, timezone
from uc3m_money.json_manager import JsonManager
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_manager import AccountManager

class AccountDeposit:
    """Class representing the information required for shipping of an order"""

    def __init__(self,
                 to_iban: str,
                 deposit_amount):
        self.__alg = "SHA-256"
        self.__type = "DEPOSIT"
        self.__to_iban = to_iban
        self.__deposit_amount = deposit_amount
        justnow = datetime.now(timezone.utc)
        self.__deposit_date = datetime.timestamp(justnow)

    def to_json(self):
        """returns the object data in json format"""
        return {"alg": self.__alg,
                "type": self.__type,
                "to_iban": self.__to_iban,
                "deposit_amount": self.__deposit_amount,
                "deposit_date": self.__deposit_date,
                "deposit_signature": self.deposit_signature}

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + str(self.__alg) +",typ:" + str(self.__type) +",iban:" + \
               str(self.__to_iban) + ",amount:" + str(self.__deposit_amount) + \
               ",deposit_date:" + str(self.__deposit_date) + "}"

    @property
    def to_iban(self):
        """Property that represents the product_id of the patient"""
        return self.__to_iban

    @to_iban.setter
    def to_iban(self, value):
        self.__to_iban = value

    @property
    def deposit_amount(self):
        """Property that represents the order_id"""
        return self.__deposit_amount
    @deposit_amount.setter
    def deposit_amount(self, value):
        self.__deposit_amount = value

    @property
    def deposit_date(self):
        """Property that represents the phone number of the client"""
        return self.__deposit_date
    @deposit_date.setter
    def deposit_date( self, value ):
        self.__deposit_date = value


    @property
    def deposit_signature( self ):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @staticmethod
    def deposit_into_account(input_file: str) -> str:
        """Processes a deposit request, reading from input and saving to storage"""

        deposit_requests = JsonManager(input_file).read_json()
        if not isinstance(deposit_requests, list) or not deposit_requests:
            raise AccountManagementException("Excepción: El JSON no tiene la estructura esperada.")

        json_salida = JsonManager("RF2/deposit_store.json")
        deposit_json = json_salida.read_json()
        deposit_signature = ""
        for request in deposit_requests:
            if not isinstance(request, dict) or "IBAN" not in request or "AMOUNT" not in request:
                raise AccountManagementException(
                    "Excepción: El JSON no tiene la estructura esperada.")


            to_iban = request["IBAN"]
            deposit_amount = request["AMOUNT"]

            if not AccountManager.validate_iban(to_iban):
                raise AccountManagementException(
                    "Excepción: Los datos del JSON no tienen valores válidos.")

            amount = validate_amount_rf2(deposit_amount)

            try:
                deposit = AccountDeposit(to_iban=to_iban, deposit_amount=amount)
                deposit_signature = deposit.deposit_signature
            except Exception as exception:
                raise AccountManagementException(
                    "Excepción: Error de procesamiento interno al obtener el deposit_signature.")\
                    from exception

            dict_json = {
                "to_iban": deposit.to_iban,
                "deposit_amount": deposit.deposit_amount,
                "deposit_date": deposit.deposit_date,
                "deposit_signature": deposit_signature
            }

            deposit_json.append(dict_json)
            json_salida.write_json(deposit_json)

        return deposit_signature


def validate_amount_rf2(amount_rf2: str):
    """Validates the amount format RF2 (e.g., EUR1234.56)"""
    try:
        if not isinstance(amount_rf2, str) or not amount_rf2.startswith("EUR"):
            raise ValueError
        cantidad = amount_rf2[3:]
        digitos = cantidad.split(".")
        if len(digitos) != 2 or not (digitos[0].isdigit() and digitos[1].isdigit()):
            raise ValueError
        if len(digitos[0]) != 4 or len(digitos[1]) != 2:
            raise ValueError
        amount = float(cantidad)
        if amount < 0:
            raise ValueError
        return amount
    except ValueError as exception:
        raise AccountManagementException(
            "Excepción: Los datos del JSON no tienen valores válidos.") from exception

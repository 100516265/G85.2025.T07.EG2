"""Contains the class OrderShipping"""
from datetime import datetime, timezone
import hashlib
from unicodedata import digit

from .json_manager import JsonManager
from .account_management_exception import AccountManagementException
from .account_manager import AccountManager

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
    def validate_amountRF2(amount_rf2: str):

        if (not isinstance(amount_rf2, str) or not amount_rf2.startswith("EUR")):
            return

        cantidad = amount_rf2[3:]
        if "." not in cantidad:
            return None

        digitos = cantidad.split(".")

        if len(digitos) != 2:
            return None

        if len(digitos[0]) != 4 or not digitos[0].isdigit():
            return None

        if len(digitos[1]) != 2 or not digitos[1].isdigit():
            return None

        try:
            amount = float(cantidad)
            if amount < 0:
                return None
            return amount
        except ValueError:
            return None

    @staticmethod
    def deposit_into_account(input_file: str) -> str:
        """Processes a deposit request, reading from input and saving to storage"""
        # Leyendo el JSON deposit_request
        deposit_requests = JsonManager(input_file).read_json()
        if not isinstance(deposit_requests, list):
            raise AccountManagementException("Excepción: El JSON no tiene la estructura esperada.")

       #leyendo el json de salida
        json_salida = JsonManager("RF2/deposit_store.json")
        deposit_json = json_salida.read_json()

        if not deposit_requests or deposit_requests == {}:
            raise AccountManagementException("JSON vacío")

        for request in deposit_requests:
            if "IBAN" not in request or "AMOUNT" not in request:
                raise AccountManagementException("Excepción: El JSON no tiene la estructura esperada.")

            to_iban = request["IBAN"]
            deposit_amount = request["AMOUNT"]

        # VALIDA IBAN
        if not AccountManager.validate_iban(to_iban):
            raise AccountManagementException("Excepcion: Los datos del JSON no tienen valores válidos.")

        #VALIDA AMOUNT
        deposit_amount = AccountDeposit.validate_amountRF2(deposit_amount)
        if deposit_amount is None:
            raise AccountManagementException("Excepción: Los datos del JSON no tienen valores válidos.")


        # SI YA EXISTE LANZA EXCEPTION
        for datos in deposit_json:
            if datos["to_iban"] == to_iban and datos["deposit_amount"] == deposit_amount:
                raise AccountManagementException("Error, la transacción ya existe")

        # Crear una instancia de AccountDeposit
        try:
            deposit = AccountDeposit(to_iban=to_iban, deposit_amount=deposit_amount)
            deposit_signature = deposit.deposit_signature
        except Exception:
            raise AccountManagementException("Exception: Error de procesamiento interno al obtener el deposit_signature.")

        #creando los datos a escribir en el archivo JSON

        dict_json = {
            "to_iban": deposit.to_iban,
            "deposit_amount": deposit.deposit_amount,
            "deposit_date": deposit.deposit_date,
            "deposit_signature": deposit_signature
        }

        deposit_json.append(dict_json)
        json_salida.write_json(deposit_json)

        return deposit_signature
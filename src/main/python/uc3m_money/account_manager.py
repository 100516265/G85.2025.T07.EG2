"""AccountManager class for managing the orders"""
from datetime import datetime, timezone
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.transfer_request import TransferRequest
from uc3m_money.json_manager import JsonManager


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
        """Valida el concepto de la transferencia"""
        if not isinstance(concept, str) or not 10 <= len(concept) <= 30:
            return False
        #dividimos el concepto en palabras
        palabras = concept.split()

        #comprueba que sean dos o mas cadenas
        if len(palabras) < 2:
            return False

        #comprobamos que cada palabra solo tenga caracteres [a-zA-Z]
        for palabra in palabras:
            for char in palabra:
                if not( 'a' <=char <= 'z' or 'A' <= char <= 'Z' ):
                    return False
        return True


    @staticmethod
    def validate_type(tipo: str) ->bool:
        """Valida el tipo de transferencia"""
        if not isinstance(tipo, str):
            return False
        if tipo in ["ORDINARY", "URGENT", "INMEDIATE"]:
            return True
        return False

    @staticmethod
    def validate_date(date: str) -> bool:
        """Valida la fecha de la transferencia"""
        if not isinstance(date, str):
            return False

        try:
            fecha_valida = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            return False

        hoy = datetime.today()

        return (
                fecha_valida >= hoy
                and 1 <= fecha_valida.day <= 31
                and 1 <= fecha_valida.month <= 12
                and 2025 <= fecha_valida.year <= 2050
        )

    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Valida la cantidad de la transferencia"""
        if (not isinstance(amount, float)) or not 10.00 <= amount <= 10000.00:
            return False

        return len(str(amount).split(".")[1] ) <= 2

    @staticmethod
    def calculate_balance(iban: str)->bool:
        """Calcula el saldo de una cuenta"""
        #VERIFICA EL IBAN
        if not isinstance(iban, str):
            return False

        if not AccountManager.validate_iban(iban):
            raise AccountManagementException(
                "Excepción: La cadena de entrada no contiene un IBAN válido.")

        transactions = JsonManager("RF3/transactions.json").read_json()
        if not transactions:
            raise AccountManagementException(
                "Excepción:Error de procesamiento interno al procesar el código")

        saldo = 0

        if transactions[0] == {}:
            raise AccountManagementException(
                "Excepción: El IBAN no se encuentra en el fichero de movimiento")

        iban_encontrado = False
        for data in transactions:

            if data["IBAN"] == iban:
                if data["amount"][0] == "+":
                    saldo = saldo + float(data["amount"][1:])
                else:
                    saldo = saldo - float(data["amount"][1:])
                iban_encontrado = True

        if not iban_encontrado:
            raise AccountManagementException(
                "Excepcion: El IBAN no se encuentra en el fichero de movimiento")

        justnow = datetime.now(timezone.utc)
            # Creando los datos a escribir en el archivo JSON
        dict_json = {
            'IBAN': iban,
            'SALDO': saldo,
            'FECHA ACTUAL': datetime.timestamp(justnow)
        }

        json_manager = JsonManager("RF3/saldos.json")
        # Adjuntamos a los datos leidos del archivo JSON
        json_manager.write_json(dict_json)
        return True

    @staticmethod
    def balance_esperado(iban):
        """Calcula el saldo esperado de una cuenta"""
        saldos = JsonManager("RF3/saldos.json")
        json_manager = JsonManager(saldos).read_json()

        balance = 0
        for transaction in json_manager:
            if transaction["IBAN"] == iban:
                balance += transaction["amount"]
        return balance

    # pylint: disable=too-many-arguments
    def transfer_request(self, from_iban: str, to_iban: str,
                         concept: str, amount: float, date: str, tipo: str) -> str:
        """Crea una solicitud de transferencia"""
        #VALIDACIONES
        if not self.validate_iban(from_iban):
            raise AccountManagementException(
                "Excepción: Los números de cuenta (from) recibidos no son válidos.")

        if not self.validate_iban(to_iban):
            raise AccountManagementException(
                "Excepcion: Los números de cuenta (to) recibidos no son válidos.")

        if not self.validate_concept(concept):
            raise AccountManagementException(
                "Excepción: El concepto no tiene un valor válido.")

        if not self.validate_type(tipo):
            raise AccountManagementException(
                "Excepción: El tipo de transferencia no es válido.")

        if not self.validate_date(date):
            raise AccountManagementException(
                "Excepción: La fecha de la transferencia no es válida.")

        if not self.validate_amount(amount):
            raise AccountManagementException(
                "Excepción: La cantidad no es válida.")

        # Crea una instancia de TransferRequest
        transfer = TransferRequest(
            from_iban=from_iban,
            transfer_type=tipo,
            to_iban=to_iban,
            transfer_concept=concept,
            transfer_date=date,
            transfer_amount=amount
        )

        # Leemos el json para ver si existe la transferencia
        json_manager = JsonManager("RF1/transfer_requests.json")
        datos_json = json_manager.read_json()
        for datos in datos_json:
            if datos['transfer_code'] == transfer.transfer_code:
                raise AccountManagementException("Error, la transferencia ya existe")

        # Creando los datos a escribir en el archivo JSON
        dict_json = {
            'from_iban': transfer.from_iban,
            'to_iban': transfer.to_iban,
            'transfer_type': transfer.transfer_type,
            'transfer_concept': transfer.transfer_concept,
            'transfer_date': transfer.transfer_date,
            'transfer_amount': transfer.transfer_amount,
            'time_stamp': transfer.time_stamp,
            'transfer_code': transfer.transfer_code
        }

        # Adjuntamos a los datos leidos del archivo JSON
        datos_json.append(dict_json)
        json_manager.write_json(datos_json)

        # Devolvemos el hash MD5
        return transfer.transfer_code

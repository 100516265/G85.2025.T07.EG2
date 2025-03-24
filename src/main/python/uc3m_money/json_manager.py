"""Este módulo se encarga de la gestión de los archivos json,
 permitiendo la lectura y escritura de los mismos."""
import hashlib
import pathlib
import json
import os
from uc3m_money.account_management_exception import AccountManagementException


class JsonManager:
    """Clase que se encarga de la gestión de los archivos json"""
    def __init__(self, path):
        self.path = path
        # Obteniendo ruta de JsonFiles de forma más sencilla mediante string
        self.str_path = pathlib.Path(__file__).resolve().parents[3] / "JsonFiles"
        # Creando el string de la ruta del archivo json
        self.json_path = self.str_path / path

    def generate_hash(self):
        """Genera un hash a partir del archivo"""
        with open(self.json_path, "rb") as file:
            return hashlib.md5(file.read()).hexdigest()

    def read_json(self):
        """Lee el archivo json"""
        try:
            with open(self.json_path, "r", encoding="utf-8", newline="") as file:
                datos_json = file.read().strip()
                if not datos_json:
                    return []
                datos = json.loads(datos_json)
        except FileNotFoundError:
            datos = []
        except json.JSONDecodeError as exception:
            raise AccountManagementException("ERROR: FORMATO JSON INCORRECTO.") from exception
        except Exception as exception:
            raise AccountManagementException("ERROR: NO SE PUEDE LEER EL JSON.") from exception
        return datos


    def write_json(self, datos):
        """Escribe en el archivo json"""
        try:
            with open(self.json_path, "w", encoding="utf-8", newline="") as file:
                # noinspection PyTypeChecker
                json.dump(datos, file, indent=2)
        except FileNotFoundError as exception:
            raise AccountManagementException (
                "ERROR: ARCHIVO JSON DAÑADO O RUTA NO ENCONTRADA.") from exception
        except json.JSONDecodeError as exception:
            raise AccountManagementException (
                "ERROR: FORMATO JSON INCORRECTO.") from exception
        except Exception as exception:
            raise AccountManagementException (
                "ERROR: NO SE HA PODIDO ESCRIBIR EL JSON.") from exception
        return datos

    def bien_registrado(self, transfer_code):
        """Comprueba si la transferencia se guardo correctamente en el json"""
        transferencia = self.read_json()

        for trans in transferencia:
            if trans["transfer_code"] == transfer_code:
                return True
        return False

    def bien_registrado_rf2(self, deposit_signature):
        """Comprueba si la transferencia se guardo correctamente en el json"""
        transferencia = self.read_json()

        for trans in transferencia:
            if trans["deposit_signature"] == deposit_signature:
                return True
        return False

    def delete(self):
        """Borra el archivo json"""
        try:
            os.remove(self.json_path)
        except FileNotFoundError as exception:
            raise AccountManagementException(
                "ERROR: ARCHIVO JSON NO ENCONTRADO.") from exception
        except Exception as exception:
            raise AccountManagementException(
                "ERROR: NO SE HA PODIDO BORRAR EL JSON.") from exception
        return True

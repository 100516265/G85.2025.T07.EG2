from .account_management_exception import AccountManagementException
from pathlib import Path
import json
import os


class JsonManager:
    def __init__(self, path):
        self.path = path
        # Obteniendo ruta de JsonFiles de forma más sencilla mediante string
        self.str_path = Path(__file__).resolve().parents[3] / "JsonFiles"
        # Creando el string de la ruta del archivo json
        self.json_path = self.str_path / path

    def read_json(self):
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
        try:
            with open(self.json_path, "w", encoding="utf-8", newline="") as file:
                json.dump(datos, file, indent=2)
        except FileNotFoundError as exception:
            raise AccountManagementException ("ERROR: ARCHIVO JSON DAÑADO O RUTA NO ENCONTRADA.") from exception
        except json.JSONDecodeError as exception:
            raise AccountManagementException ("ERROR: FORMATO JSON INCORRECTO.") from exception
        except Exception as exception:
            raise AccountManagementException ("ERROR: NO SE HA PODIDO ESCRIBIR EL JSON.") from exception
        return datos

    #comprueba si esta bien registrado la transferencia
    def bien_registrado(self, transfer_code):

        transferencia = self.read_json()

        for trans in transferencia:
            if trans["transfer_code"] == transfer_code:
                return True
        return False
    def bien_registrado_RF2(self, deposit_signature):

        transferencia = self.read_json()

        for trans in transferencia:
            if trans["deposit_signature"] == deposit_signature:
                return True
        return False

    #Comprueba si se modifico el json,si no se guardo nada en el json
    def comprobar_json(self, json_inicial):

        json_final=len(self.read_json())
        return json_final==json_inicial


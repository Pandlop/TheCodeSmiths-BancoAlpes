from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_keys():

    # Generar el par de llaves asimetricas
    llavePrivada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Obtener la llave pública desde la llave privada
    llavePublica = llavePrivada.public_key()

    # Serializar la llave privada
    pemPrivada = llavePrivada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serializar la llave pública
    pemPublica = llavePublica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Guardar la llave privada en un archivo
    with open('llavePrivada.pem', 'wb') as f:
        f.write(pemPrivada)

    # Guardar la llave pública en un archivo
    with open('llavePublica.pem', 'wb') as f:
        f.write(pemPublica)

    print("Llaves generadas y guardadas con éxito.")

if __name__ == "__main__":
    generate_keys()

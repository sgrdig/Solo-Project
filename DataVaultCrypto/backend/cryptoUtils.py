from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding



class cryptoUtils:
    def __init__(self):

        self.privateKeys = None 
        self.publicKeys = None

    def saveKeys(self) -> str:
        """ Def qui sauvegarde les clés privées et publiques dans des fichiers PEM."""
        try:
            private_pem = self.privateKeys.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )

            public_pem = self.publicKeys.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )

            with open("private_key.pem", "wb") as priv_file:
                priv_file.write(private_pem)

            with open("public_key.pem", "wb") as pub_file:
                pub_file.write(public_pem)

            return "private_key.pem"

        except Exception as e:
            print(f"Erreur lors de la sauvegarde des clés : {e}")
            return None
        

    def generatekeys(self):
        """ Def qui genere les clés privées et publiques """

        try :
            print("Generating new keys...")
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=4096,
            )
            self.privateKeys = private_key
            self.publicKeys = private_key.public_key()
            

            fileName = self.saveKeys()
            if fileName:
                print(f"Clés sauvegardées avec succès ! Fichier : {fileName}")
                print("Keys generated successfully.")

        except Exception as e:
            print(f"Error generating keys: {e}")

    def loadKeys(self, private_key_path: str, public_key_path: str):
        """ Def qui charge les clés privées et publiques à partir de fichiers PEM."""
        try:
            with open(private_key_path, "rb") as priv_file:
                self.privateKeys = serialization.load_pem_private_key(
                    priv_file.read(),
                    password=None,
                )

            with open(public_key_path, "rb") as pub_file:
                self.publicKeys = serialization.load_pem_public_key(
                    pub_file.read()
                )

            print("Clés chargées avec succès.")
        except Exception as e:
            print(f"Erreur lors du chargement des clés : {e}")



    def encryptData(self , data : str):
        """ Def qui  encrypt la data"""
        try :
            if self.publicKeys is None or self.privateKeys is None:
                raise ValueError("One or both Key(s) are not loaded.")
            encrypted_data = self.publicKeys.encrypt(
                data.encode(),
                padding =padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                )
            )
            
            print("Data encrypted successfully.")
            with open("encrypted_data.bin", "wb") as enc_file:
                enc_file.write(encrypted_data)


            return encrypted_data
             
        except ValueError as ve:
            print(f"Error: {ve}")
            return None

        except Exception as e:
            print(f"Error lors de l'encryption de vos data: {e}")
            return None
        
    def decryptData(self, encrypted_data, from_file=False):
        """ Def qui decrypt la data ou un fichier bin """
        
        try:
            if self.privateKeys is None:
                raise ValueError("Private key is not loaded.")

            if from_file:
                with open(encrypted_data, "rb") as enc_file:
                    encrypted_data = enc_file.read()

            decrypted_data = self.privateKeys.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                )
            )

            print("Data decrypted successfully.")
            print("Decrypted data: ", decrypted_data.decode())
            return decrypted_data.decode()

        except ValueError as ve:
            print(f"Error: {ve}")
            return None

        except Exception as e:
            print(f"Error during decryption: {e}")
            return None

            
# c  =cryptoUtils()
# c.generatekeys()
# c.encryptData("hello world")
# c.decryptData("encrypted_data.bin", from_file=True)

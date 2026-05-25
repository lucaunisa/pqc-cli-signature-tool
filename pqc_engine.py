import oqs
import base64

class PQCEngine:
    def __init__(self, alg_name="Dilithium3"):
        # Verifichiamo se l'algoritmo è supportato dalla libreria liboqs [cite: 84, 128]
        if alg_name not in oqs.get_enabled_sig_mechanisms():
            raise ValueError(f"Algoritmo {alg_name} non supportato.")
        self.alg_name = alg_name

    def keygen(self):
        """Genera una coppia di chiavi (pubblica e privata)"""
        with oqs.Signature(self.alg_name) as sig:
            public_key = sig.generate_keypair()
            private_key = sig.export_secret_key()
            # Restituisco le chiavi codificate in Base64
            return {
                "public_key": base64.b64encode(public_key).decode('utf-8'),
                "private_key": base64.b64encode(private_key).decode('utf-8')
            }

    def sign(self, message, private_key_b64):
        """Firma un messaggio (o contenuto di un file)"""
        private_key = base64.b64decode(private_key_b64)
        
        with oqs.Signature(self.alg_name, secret_key=private_key) as sig:
            signature = sig.sign(message)
            # Restituiamo la firma in Base64
            return base64.b64encode(signature).decode('utf-8')

    def verify(self, message, signature_b64, public_key_b64):
        """Verifica la validità della firma [cite: 150, 152]"""
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        with oqs.Signature(self.alg_name) as sig:
            try:
                is_valid = sig.verify(message, signature, public_key)
                return is_valid
            except Exception:
                return False
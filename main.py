import sys
from pqc_engine import PQCEngine

def main():
    # Inizializziamo il motore con Dilithium3 (puoi cambiarlo con Dilithium2 o 5)
    engine = PQCEngine(alg_name="Dilithium3")

    print("--- Prototipo Firma Digitale PQC ---")
    print("1. Keygen (Genera Chiavi)")
    print("2. Sign (Firma un messaggio)")
    print("3. Verify (Verifica Firma)")
    
    scelta = input("\nScegli un'opzione (1/2/3): ")

    if scelta == "1":
        print("\n[Esecuzione Keygen...]")
        chiavi = engine.keygen()
        print(f"Chiave Pubblica (primi 30 car.): {chiavi['public_key'][:30]}...")
        print(f"Chiave Privata (primi 30 car.): {chiavi['private_key'][:30]}...")
        
        # Salvataggio su file (Fase 4 - Persistenza)
        with open("public_key.pem", "w") as f:
            f.write(chiavi['public_key'])
        with open("private_key.pem", "w") as f:
            f.write(chiavi['private_key'])
        print("\nChiavi salvate correttamente in 'public_key.pem' e 'private_key.pem'")

    elif scelta == "2":
        msg = input("Inserisci il messaggio da firmare: ").encode()
        try:
            with open("private_key.pem", "r") as f:
                pk_b64 = f.read()
            firma = engine.sign(msg, pk_b64)
            with open("signature.dat", "w") as f:
                f.write(firma)
            print(f"\nMessaggio firmato! Firma salvata in 'signature.dat'")
        except FileNotFoundError:
            print("Errore: Genera prima le chiavi (Opzione 1).")

    elif scelta == "3":
        msg = input("Inserisci il messaggio da verificare: ").encode()
        try:
            with open("public_key.pem", "r") as f:
                pub_b64 = f.read()
            with open("signature.dat", "r") as f:
                sig_b64 = f.read()
            
            valida = engine.verify(msg, sig_b64, pub_b64)
            if valida:
                print("\n✅ FIRMA VALIDA: Il messaggio è autentico.")
            else:
                print("\n❌ FIRMA NON VALIDA: Il messaggio o la chiave sono errati.")
        except FileNotFoundError:
            print("Errore: File chiavi o firma mancanti.")

if __name__ == "__main__":
    main()
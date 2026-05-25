import time
import os
import oqs
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def run_benchmark():
    # 1. Configurazione: File da 100KB, 1MB e 10MB
    file_sizes_mb = [0.1, 1, 10] 
    alg_pqc = "Dilithium3"
    
    print("="*60)
    print(f"VALUTAZIONE SPERIMENTALE: RSA-2048 vs {alg_pqc}")
    print("="*60)
    
    # --- FASE 1: GENERAZIONE CHIAVI ---
    # RSA
    start = time.time()
    rsa_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    rsa_keygen_time = time.time() - start
    
    # PQC (Dilithium3)
    start = time.time()
    with oqs.Signature(alg_pqc) as sig:
        pqc_public_key = sig.generate_keypair()
        pqc_private_key = sig.export_secret_key()
    pqc_keygen_time = time.time() - start

    print(f"\n[METRICA 1] TEMPO GENERAZIONE CHIAVI:")
    print(f"  > RSA-2048: {rsa_keygen_time:.6f} s")
    print(f"  > {alg_pqc}:  {pqc_keygen_time:.6f} s")

    # --- FASE 2: TEST PERFORMANCE SU FILE ---
    for size in file_sizes_mb:
        print(f"\n" + "-"*40)
        print(f"TEST DIMENSIONE FILE: {size} MB")
        print("-"*40)
        
        # Generazione dati casuali
        data = os.urandom(int(size * 1024 * 1024))
        
        # --- FIRMA ---
        # RSA
        start = time.time()
        rsa_sig = rsa_private_key.sign(data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        rsa_sign_t = time.time() - start
        
        # PQC
        with oqs.Signature(alg_pqc, secret_key=pqc_private_key) as sig:
            start = time.time()
            pqc_sig = sig.sign(data)
            pqc_sign_t = time.time() - start
        
        # --- VERIFICA ---
        # RSA
        start = time.time()
        rsa_private_key.public_key().verify(rsa_sig, data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        rsa_verify_t = time.time() - start
        
        # PQC
        with oqs.Signature(alg_pqc) as sig:
            start = time.time()
            sig.verify(data, pqc_sig, pqc_public_key)
            pqc_verify_t = time.time() - start

        print(f"FIRMA    | RSA: {rsa_sign_t:.6f}s | PQC: {pqc_sign_t:.6f}s")
        print(f"VERIFICA | RSA: {rsa_verify_t:.6f}s | PQC: {pqc_verify_t:.6f}s")

    print("\n" + "="*60)
    print("Benchmark completato. Copia questi dati nella Relazione (Cap. 6).")
    print("="*60)

if __name__ == "__main__":
    run_benchmark()
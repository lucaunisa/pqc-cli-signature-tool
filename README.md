# Post-Quantum Cryptography (PQC) CLI & Benchmarking Tool

A Python-based suite designed and implemented during my curricular internship at the University of Salerno (UNISA). This repository bridges theoretical cryptographic research with practical application security, focusing on quantum-resistant digital signatures and comparative performance evaluation.

## 🚀 Core Features
- **NIST Standard Integration:** Native integration with Open Quantum Safe (`liboqs`) utilizing the **Crystals-Dilithium3** lattice-based signature scheme (Level 3 Security).
- **Signature Lifecycle Management:** Complete interactive workflow via CLI for secure Key Generation, message/file signing, and strict verification logic (handling correct/tampered inputs).
- **Experimental Benchmarking Suite:** Built-in module (`benchmark_pqc.py`) to systematically compare **RSA-2048** vs **Dilithium3** performance across multiple payload sizes (0.1MB, 1MB, 10MB), tracking computation times for Keygen, Signing, and Verification.
- **Future-Proof Audit Design:** Structured CLI outputs and execution logs are architecture-ready to feed machine learning models (e.g., Anomaly Detection) for automated, intelligent security auditing.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Cryptography Libraries:** `liboqs`, `liboqs-python`, `cryptography`
- **Security Domains:** Post-Quantum Cryptography (PQC), Performance Benchmarking, Systems Telemetry.

## ⚙️ Quick Start
1. Ensure the `liboqs` C library is properly configured on your system architecture.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

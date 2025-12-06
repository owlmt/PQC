# Backdooring Post-Quantum Cryptography

### Experimental Implementations and Reproductions

This repository contains a series of controlled security experiments exploring **kleptographic backdoors** in **post-quantum cryptographic (PQC) algorithms**, with a primary focus on **ML-KEM (Kyber)**.
The purpose of this project is **research and education**: to understand how implementation-level channels can subvert PQC schemes, even when the mathematical construction is secure.

---

## Experiment 1

### Backdoor in ML-KEM Key Generation (based on *Backdooring Post-Quantum Cryptography*, GLSVLSI ’24)

Paper:
**Backdooring Post-Quantum Cryptography**
ACM GLSVLSI 2024
[https://dl.acm.org/doi/10.1145/3649476.3660373](https://dl.acm.org/doi/10.1145/3649476.3660373)

This experiment reproduces the core idea of the paper’s **Algorithm 2**, where a malicious implementation of ML-KEM key generation leaks the full secret key by embedding a covert payload inside the public key.

The attack uses a secondary cryptosystem (in the paper: **ECDH over K-409**) to construct a ciphertext `ct_bd`. The encrypted value’s first 32 bytes (`seed_B`) are used to deterministically generate the PQC secret key `s`. The ciphertext itself is **hidden inside the Kyber public key** by modifying the LWE component
[
t = A \cdot s + e
]
into a backdoored version
[
t' = t + h
]
such that
[
t'[i] \equiv p[i] \pmod{2^{c_{\text{bits}}}}
]
where (p[i]) encodes the ciphertext bits.

An external attacker, who knows the ECDH private key, can:

1. Read the public key.
2. Extract `ct_bd` via modular reconstruction of (t').
3. Decrypt it to obtain `seed_B`.
4. Recompute the full Kyber secret `s`.

### Provided in this repository

* A **Python implementation** of a backdoored ML-KEM core (key generation only).
* Faithful reproduction of Equation (1), compensation vectors, and recovery logic.
* Real polynomial arithmetic in (R_q).
* CBD sampling consistent with FIPS 203.
* A working end-to-end recovery demonstration.

This experiment does **not** re-implement the full FIPS-203 KEM (Encaps/Decaps).
Its goal is to isolate and demonstrate the **kleptographic channel** in a minimal, readable form.

---

## Warning / Disclaimer

This repository is for:

* **Academic research**
* **Security analysis**
* **Understanding implementation-level risks in PQC**

It is **not** intended for deployment or integration into real systems.
Never use modified, experimental, or untrusted cryptographic implementations in production.



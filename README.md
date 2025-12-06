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

## Experiment 2

### Backdoor in Kyber-KEM via Conditional Error Sampling

*(based on* **Post-Quantum Backdoor for Kyber-KEM**, *LNCS WISA 2025)*

Paper:
**Post-Quantum Backdoor for Kyber-KEM**
LNCS 2025 (WISA Proceedings)
[https://link.springer.com/chapter/10.1007/978-3-031-82852-2_11](https://link.springer.com/chapter/10.1007/978-3-031-82852-2_11)

Reference Code (authors):
[https://github.com/Summwer/kyber-backdoor](https://github.com/Summwer/kyber-backdoor)

CyberSeQ Python Simulation (Experiment 2 reproduction):
[https://github.com/owlmt/PQC/blob/main/mlkem_backdoor_experiment2.ipynb](https://github.com/owlmt/PQC/blob/main/mlkem_backdoor_experiment2.ipynb)

This experiment implements the backdoor proposed by Xia, Wang, and Gu in 2025, which introduces a **statistically undetectable kleptographic channel** directly inside **Kyber-KEM**.
Unlike Experiment 1, which uses modular compensation vectors, this attack uses **conditional sampling of the noise vector `e`** to embed an auxiliary ciphertext inside the **LSBs of the Kyber public key**.

The attacker uses a secondary post-quantum system (in the paper: **Classic McEliece**) to produce:

1. A **768-bit ciphertext** `C`.
2. A shared secret `K`, which acts as the deterministic seed `d` for Kyber key generation.

Kyber’s public key component is:

[
t = A \cdot s + e
]

The backdoor modifies the sampling of `e` such that:

* If `LSB(A·s[i]) = C[i]`, sample `e[i]` from **D₀** (even-valued errors).
* If `LSB(A·s[i]) ≠ C[i]`, sample `e[i]` from **D₁** (odd-valued errors).

This ensures that for all **non-border coefficients**:

[
\operatorname{LSB}(t[i]) = C[i]
]

with probability 1, while the global error distribution still matches the true **B₂** distribution used in FIPS 203.

An external party holding the **McEliece secret key** can:

1. Read the Kyber public key.
2. Extract the bitstring `C` by reading the LSBs of `t`.
3. Decrypt `C` to recover the seed `K`.
4. Recompute the Kyber secret vector `s`, fully recovering the private key.

### Provided in this repository

* A **full Python implementation** of the Xia–Wang–Gu KeyGen* and KeyRec* algorithms.
* Deterministic, Kyber-consistent sampling of the B₂ noise distribution.
* Real matrix–vector arithmetic in (R_q) with centered representation.
* Verification of:

  * conditional error distributions (D₀, D₁),
  * border-case frequency,
  * LSB uniformity.
* A complete **end-to-end recovery demo**, where the attacker:

  * extracts `C`,
  * decrypts it via Classic McEliece,
  * regenerates the Kyber secret key.

This experiment demonstrates how a **fully standards-compliant** ML-KEM implementation can be backdoored without altering any observable statistical properties of the public key or noise distribution.
Because the attack lives entirely inside **KeyGen**, and preserves the expected randomness profile, traditional conformance tests cannot detect it.

---

## Warning / Disclaimer

This repository is for:

* **Academic research**
* **Security analysis**
* **Understanding implementation-level risks in PQC**

It is **not** intended for deployment or integration into real systems.
Never use modified, experimental, or untrusted cryptographic implementations in production.




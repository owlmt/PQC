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

CyberSeQ Python Simulation:
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
## Experiment 3
### Backdoor in CRYSTALS-Dilithium (ML-DSA) via Parity Encoding

_*(based on Algorithms 4–6 from “Backdooring Dilithium Signatures”)_

Paper:
Backdooring Dilithium Signatures via Parity Leakage
https://link.springer.com/chapter/10.1007/978-3-031-83885-9_30

Reference Code (authors):
N/A (no official implementation released)

CyberSeQ Python Simulation:
https://github.com/owlmt/PQC/blob/main/mldsa_backdoor_experiment1.ipynb

---

## Overview

This experiment reproduces the **kleptographic backdoor** described in the parity-based encoding mechanism of Algorithms 4–6 from the referenced Dilithium backdoor paper.

Unlike Experiments 1 and 2 (which target ML-KEM), this attack compromises **ML-DSA / CRYSTALS-Dilithium**, the FIPS-204 standard for post-quantum signatures.

The key idea:

**A malicious implementation can encode an arbitrary secret payload inside the vector `z` of a Dilithium signature simply by controlling the parity of its coefficients.**

The legitimate signature still passes verification, and the attack does not modify or violate the mathematical structure of Dilithium.

---

## How the Attack Works

A Dilithium signature contains:

```
(z, h, c)
```

The backdoor replaces the honest computation of `z` with a controlled process that encodes attacker-chosen data.

### 1. Mask the message

```
M_rho = M XOR rho
```

* `x ∈ {0,1}` controls parity inversion
* `rho ∈ {0,1}^θ` is a random mask

### 2. Encode parity

For each coefficient `z[i]`:

* If an **even** number is needed → sample from even residues modulo `q`.
* If an **odd** number is needed → sample from odd residues modulo `q`.

This enforces:

```
parity(z[i]) XOR x = M_rho[i]
```

### 3. Rejection sampling keeps the signature valid

The attacker regenerates coefficients until Dilithium’s rejection conditions pass.
Verification remains completely unchanged.

### 4. Decode

An attacker with `(x, rho)` recovers the hidden message:

```
M[i] = (parity(z[i]) XOR x) XOR rho[i]
```

Recovery is exact and deterministic.

---

## Hybrid Extension (Provided Here)

The paper supports only:

```
θ ≤ 255*k − 1
```

This repository extends the attack to **any message length**:

### Short messages

Encoded fully via parity (Algorithm 6).

### Long messages

Split into two parts:

* `M1` → encoded via parity
* `M2` → indexes of `1` bits are recorded

### Embedding strategy

If unused room exists inside `z`, the index list of `M2` is hidden inside the unused coefficients.
Otherwise, `M2` is returned separately (academic-mode reproduction of paper).

This makes the experiment fully expressive and demonstrates real-world exfiltration capability.

---

## Why This Attack Matters

This backdoor:

* Does not modify Dilithium’s mathematics
* Produces statistically valid signatures
* Probably passes all FIPS-204 and NIST conformance tests
* Evades distributional tests (even/odd residues remain uniform)
* Works inside TPMs, HSMs, TEEs, enclaves, firmware
* Does not require modification to public API or signature structure

**A malicious library or hardware implementation could leak:**

* private messages
* authentication tokens
* one-time signing keys
* internal state
* user secrets

without ever failing verification.

---

## Summary

Experiment 3 demonstrates that:

* ML-DSA (Dilithium) can be backdoored silently
* The parity of the `z` coefficients is enough to leak arbitrary data
* Verification does not detect the manipulation
* Statistical tests cannot detect the manipulation
* Signatures remain fully standards-compliant

This shows the profound risk of **implementation-level backdoors** in post-quantum signature schemes and motivates **formal verification** of cryptographic implementations, HSM firmware, and secure elements.

---

## Warning / Disclaimer

This repository is for:

* **Academic research**
* **Security analysis**
* **Understanding implementation-level risks in PQC**

It is **not** intended for deployment or integration into real systems.
Never use modified, experimental, or untrusted cryptographic implementations in production.







// High risk: RSA with SHA-1 signatures. SHA-1 is collision-broken; signatures are no longer trustworthy.
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    EVP_PKEY *pkey = NULL;
    RSA *rsa = RSA_new();
    BIGNUM *e = BN_new(); BN_set_word(e, RSA_F4);
    RSA_generate_key_ex(rsa, 1024, e, NULL);  // weak key size
    pkey = EVP_PKEY_new(); EVP_PKEY_assign_RSA(pkey, rsa); // pkey owns rsa

    const unsigned char msg[] = "SHA-1 RSA legacy demo";
    unsigned char sig[256]; size_t siglen = sizeof sig;

    EVP_MD_CTX *ctx = EVP_MD_CTX_new();
    EVP_DigestSignInit(ctx, NULL, EVP_sha1(), NULL, pkey);
    EVP_DigestSignUpdate(ctx, msg, strlen((const char*)msg));
    EVP_DigestSignFinal(ctx, sig, &siglen);

    EVP_MD_CTX *vr = EVP_MD_CTX_new();
    EVP_DigestVerifyInit(vr, NULL, EVP_sha1(), NULL, pkey);
    EVP_DigestVerifyUpdate(vr, msg, strlen((const char*)msg));
    int ok = EVP_DigestVerifyFinal(vr, sig, siglen);

    printf("RSA-SHA1 signature verify=%s len=%zu\n", ok == 1 ? "OK" : "FAIL", siglen);

    EVP_MD_CTX_free(ctx); EVP_MD_CTX_free(vr);
    EVP_PKEY_free(pkey); BN_free(e);
    return 0;
}

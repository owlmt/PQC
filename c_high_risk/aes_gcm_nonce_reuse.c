// Very high risk: AES-GCM with nonce reuse under the same key on two messages.
// This compromises confidentiality and integrity.
#include <openssl/evp.h>
#include <stdio.h>
#include <string.h>

int gcm_encrypt(const unsigned char *key, const unsigned char *iv, const unsigned char *pt, int ptlen,
                unsigned char *ct, unsigned char *tag) {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    int len, ctlen;
    EVP_EncryptInit_ex(ctx, EVP_aes_128_gcm(), NULL, NULL, NULL);
    EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, 12, NULL);
    EVP_EncryptInit_ex(ctx, NULL, NULL, key, iv);
    EVP_EncryptUpdate(ctx, ct, &len, pt, ptlen); ctlen = len;
    EVP_EncryptFinal_ex(ctx, ct + len, &len); ctlen += len;
    EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, 16, tag);
    EVP_CIPHER_CTX_free(ctx);
    return ctlen;
}

int main(void) {
    const unsigned char key[16] = "GCM_WEAK_KEY__16";
    const unsigned char iv[12]  = {0,1,2,3,4,5,6,7,8,9,10,11}; // reused nonce
    const unsigned char m1[] = "first message";
    const unsigned char m2[] = "second message";
    unsigned char c1[64], t1[16], c2[64], t2[16];
    int n1 = gcm_encrypt(key, iv, m1, (int)strlen((const char*)m1), c1, t1);
    int n2 = gcm_encrypt(key, iv, m2, (int)strlen((const char*)m2), c2, t2);
    printf("AES-GCM nonce reuse produced c1_len=%d c2_len=%d\n", n1, n2);
    return 0;
}

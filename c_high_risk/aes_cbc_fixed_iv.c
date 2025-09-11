// Very high risk: AES-CBC with fixed zero IV and key reuse. IV reuse breaks semantic security.
#include <openssl/aes.h>
#include <stdio.h>
#include <string.h>

static void pkcs7_pad(const unsigned char *in, size_t inlen, unsigned char *out, size_t *outlen) {
    size_t pad = AES_BLOCK_SIZE - (inlen % AES_BLOCK_SIZE);
    memcpy(out, in, inlen);
    for (size_t i = 0; i < pad; i++) out[inlen + i] = (unsigned char)pad;
    *outlen = inlen + pad;
}

int main(void) {
    const unsigned char key[16] = "0123456789ABCDEF";   // static 128-bit key
    unsigned char iv[AES_BLOCK_SIZE] = {0};             // fixed IV (bad)
    const unsigned char msg[] = "AES-CBC legacy demo";
    unsigned char inbuf[64], ct[64], pt[64];
    size_t inlen, nbytes;

    pkcs7_pad(msg, strlen((const char*)msg), inbuf, &inlen);

    AES_KEY enc, dec; AES_set_encrypt_key(key, 128, &enc); AES_set_decrypt_key(key, 128, &dec);
    memcpy(pt, inbuf, inlen);
    memcpy(ct, inbuf, inlen);
    // Encrypt
    unsigned char iv1[AES_BLOCK_SIZE] = {0};
    AES_cbc_encrypt(inbuf, ct, inlen, &enc, iv1, AES_ENCRYPT);
    // Decrypt
    unsigned char iv2[AES_BLOCK_SIZE] = {0};
    AES_cbc_encrypt(ct, pt, inlen, &dec, iv2, AES_DECRYPT);

    // remove padding
    nbytes = pt[inlen - 1];
    pt[inlen - nbytes] = 0;
    printf("AES-CBC decrypted: %s\n", pt);
    return 0;
}

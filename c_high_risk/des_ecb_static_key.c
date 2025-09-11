// Very high risk: DES in ECB mode with a hard-coded key. Pattern leakage and weak cipher.
#include <openssl/des.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    const unsigned char key_bytes[8] = {0x13,0x34,0x57,0x79,0x9B,0xBC,0xDF,0xF1}; // static key
    DES_cblock key; memcpy(key, key_bytes, 8);
    DES_key_schedule ks; DES_set_key_unchecked(&key, &ks);

    const unsigned char pt[8] = "LEGACY12"; // single block, ECB
    DES_cblock ct, dec;

    DES_ecb_encrypt((const_DES_cblock*)pt, &ct, &ks, DES_ENCRYPT);
    DES_ecb_encrypt(&ct, &dec, &ks, DES_DECRYPT);
    printf("DES-ECB decrypted: %.8s\n", dec);
    return 0;
}
